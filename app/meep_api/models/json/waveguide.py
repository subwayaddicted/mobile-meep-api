from .waveguide_data import complete_waveguide_data_json_model

waveguide_json_model = {
    "type": "object",
    "properties": {
    },
    "required": [
        "data",
    ]
}

waveguide_json_model["properties"].update(complete_waveguide_data_json_model)