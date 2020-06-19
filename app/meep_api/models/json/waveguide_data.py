from .cell import cell_json_model
from .geometry import geometry_json_model

waveguide_data_json_model = {
    "data": {
        "type": "object",
        "properties": {
            "cell": {
                "type": "object",
                "properties": {

                }
            },
            "geometry": {
                "type": "object",
                "properties": {

                }
            },
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
                                "type": "integer"
                            },
                            "y": {
                                "type": "integer"
                            }
                        },
                        "required": [
                            "x",
                            "y"
                        ]
                    }
                },
                "required": [
                    "frequency",
                    "center"
                ]
            },
			"simulation_time": {
				"type": "object",
				"properties": {
					"between": {
						"type": "integer"
					},
					"until": {
						"type": "integer"
					}
				},
				"required": [
					"between",
					"until"
				]
			},
            "pml_layers": {
                "type": "number"
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

waveguide_data_json_model["data"]["properties"]['cell'].update(cell_json_model)
waveguide_data_json_model["data"]["properties"]['geometry'].update(geometry_json_model)

complete_waveguide_data_json_model = waveguide_data_json_model