from .cell import cell_json_model
from .geometry import geometry_cell_model

waveguide_data_json_model = {
    "data": {
        "type": "object",
        "properties": {
            "sources": {
                "type": "object",
                "properties": {
                    "frequency": {
                        "type": "number"
                    },
                    "center": {
                        "type": "object",
                        "properties": {
                            "x": {
                                "type": "string"
                            },
                            "y": {
                                "type": "string"
                            }
                        },
                        "required": [
                            "x",
                            "y"
                        ]
                    },
                    "material": {
                        "type": "integer"
                    }
                },
                "required": [
                    "frequency",
                    "center",
                    "material"
                ]
            },
            "pml_layers": {
                "type": "array",
                "items": {}
            },
            "resolution": {
                "type": "integer"
            }
        },
        "required": [
            "cell",
            "geometry",
            "sources",
            "pml_layers",
            "resolution"
        ]
    }
}

waveguide_data_json_model["data"]["properties"].update(cell_json_model)
waveguide_data_json_model["data"]["properties"].update(geometry_cell_model)