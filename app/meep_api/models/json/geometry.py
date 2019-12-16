geometry_cell_model = {
    "geometry": {
        "type": "object",
        "properties": {
            "coordinates": {
                "type": "object",
                "properties": {
                    "x": {
                        "type": "string"
                    },
                    "y": {
                        "type": "string"
                    },
                    "z": {
                        "type": "string"
                    }
                },
                "required": [
                    "x",
                    "y",
                    "z"
                ]
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
            "coordinates",
            "center",
            "material"
        ]
    }
}
