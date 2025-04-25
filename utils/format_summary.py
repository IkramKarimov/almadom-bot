def format_summary(data: dict) -> str:
    summary = (
        f"<b>Тип:</b> {data.get('type')}\n"
        f"<b>Район:</b> {data.get('district')}\n"
        f"<b>Комнаты:</b> {data.get('rooms')}\n"
        f"<b>ЖК:</b> {data.get('complex_name') or '—'}\n"
        f"<b>Адрес:</b> {data.get('address') or '—'}\n"
        f"<b>Год постройки:</b> {data.get('year')}\n"
        f"<b>Цена:</b> {data.get('price')} ₸\n"
        f"<b>Площадь:</b> {data.get('area')} м²\n"
        f"<b>Этажность:</b> {data.get('floor')}"
    )
    return summary