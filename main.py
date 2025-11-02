import json
from datetime import datetime

import connexion
from flask import request, jsonify

from Src.Convertors.structure_convertor import structure_converter
from Src.start_service import start_service
from Src.reposity import reposity
from Src.Logics.factory_entities import factory_entities
from Src.Convertors.convert_factory import convert_factory

app = connexion.FlaskApp(__name__)
service = start_service()
service.start()
factory = factory_entities()
conv_factory = convert_factory()


@app.route("/api/get_receipts", methods=['GET'])
def get_receipts():
    receipts = service.data[reposity.receipt_key()]
    _factory = convert_factory()
    converted_receipts = []
    for receipt in receipts:
        converted_receipts.append(_factory.serialize_to_json(receipt))
    return jsonify(converted_receipts)


@app.route("/api/get_receipt/<string:code>", methods=["GET"])
def get_receipt(code):
    receipt = next((r for r in service.data[reposity.receipt_key()] if r.unique_code == code), None)
    if receipt:
        _factory = convert_factory()
        return _factory.serialize_to_json(receipt)
    else:
        return jsonify({'error': "Receipt not found"}), 404


@app.route("/api/accessibility", methods=['GET'])
def accessibility():
    return "SUCCESS"


@app.route("/api/data/<entity>", methods=['GET'])
def get_data(entity):
    fmt = request.args.get('format', 'json').lower()
    key_map = {
        "nomenclature": reposity.nomenclature_key(),
        "range": reposity.range_key(),
        "receipt": reposity.receipt_key(),
        "group": reposity.group_key(),
        "storage": reposity.storage_key(),
        "transaction": reposity.transaction_key()
    }

    if entity not in key_map:
        return jsonify({"error": "Unknown entity"}), 404

    data_list = service.data[key_map[entity]]

    try:
        logic = factory.create(fmt)
        text = logic.build(fmt, data_list)
        return text, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/osv_report", methods=['GET'])
def osv_report():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    storage_id = request.args.get('storage_id')

    if not all([start_date, end_date, storage_id]):
        return jsonify({"error": "Все параметры обязательны: start_date, end_date, storage_id"}), 400


    transactions = service.data.get(reposity.transaction_key(), [])
    filtered_transactions = [
        t for t in transactions
        if t.storage.unique_code == storage_id and
           start_date <= t.date.strftime('%Y-%m-%d') <= end_date
    ]

    report = {}
    for t in filtered_transactions:
        # Генерируем строковый ключ из уникального кода номенклатуры и единицы измерения
        key = f"{t.nomenclature.unique_code}-{t.unit.unique_code}"
        if key not in report:
            report[key] = {
                'initial_balance': 0,
                'product': t.nomenclature,
                'unit': t.unit,
                'incoming': 0,
                'outgoing': 0,
                'final_balance': 0
            }

        if t.quantity > 0:
            report[key]['incoming'] += t.quantity
        else:
            report[key]['outgoing'] -= t.quantity

    for k, v in report.items():
        initial_balance = service.get_initial_balance(k.split('-')[0], start_date)
        final_balance = initial_balance + v['incoming'] - v['outgoing']
        v['initial_balance'] = initial_balance
        v['final_balance'] = final_balance

    # Готовим финальный отчет
    formatted_report = []
    for _, v in report.items():
        formatted_report.append({
            'nomenclature': v['product'],
            'unit': v['unit'],
            'initial_balance': v['initial_balance'],
            'incoming': v['incoming'],
            'outgoing': v['outgoing'],
            'final_balance': v['final_balance']
        })

    return structure_converter(conv_factory).convert(formatted_report)


@app.route("/api/save_data", methods=['POST'])
def save_data():
    filename = "example.json" #request.form.get('filename')

    if not filename:
        return jsonify({"error": "Название файла должно быть указано"}), 400

    # Получаем все данные из репозитория
    data = service.data.copy()

    # Преобразовываем все объекты в словарь
    from Src.Convertors.structure_convertor import structure_converter
    serialized_data = conv_factory.convert_object(data)

    # Сохраняем в файл
    with open(filename, 'w') as f:
        json.dump(serialized_data, f, ensure_ascii=False, indent=2)

    return jsonify({"message": "Данные сохранены успешно"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
