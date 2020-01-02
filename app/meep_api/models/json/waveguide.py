from .waveguide_data import waveguide_data_json_model

waveguide_json_model = {
    "type": "object",
    "properties": {
        "waveguide_type": {
            "type": "integer"
        }
    },
    "required": [
        "data",
        "waveguide_type"
    ]
}

waveguide_json_model["properties"].update(waveguide_data_json_model)