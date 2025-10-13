import json
from typing import Any, Type

from generate_qa_pairs.tasks import (
    base,
    booking_get_seat_map,
    booking_rooms_with_availability,
    booking_search_car_rentals,
    booking_search_hotel_by_coordinates,
    product_details_shoes,
    SEC_filings,
)


class TaskList:
    def __init__(self, api_response_fpath: str) -> None:
        self._api_response_fpath = api_response_fpath

        self.api_response = self.read_api_response()
        self.task_list = self.init_task_list()

    def init_task_list(self) -> list[Type[base.Task]]:
        raise NotImplementedError

    def read_api_response(self) -> Any:
        with open(self._api_response_fpath, "r") as f:
            return json.load(f)



class BookingGetRoomListWithAvailability(TaskList):

    response_json_schema: str = """
    {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Response schema for get room list with availability endpoint.",
    "type": "object",
    "properties": {
        "status": {
        "type": "boolean"
        },
        "available": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
            "name_without_policy": {
                "type": "string"
            },
            "nr_children": {
                "type": "number"
            },
            "max_children_free_age": {
                "type": "number"
            },
            "package_id": {
                "type": "number"
            },
            "full_board": {
                "type": "number"
            },
            "deals": {
                "type": "object",
                "properties": {
                "deal_attributes": {
                    "type": "object",
                    "properties": {
                    "has_secret_channel_option": {
                        "type": "number"
                    }
                    },
                    "required": [
                    "has_secret_channel_option"
                    ]
                }
                },
                "required": [
                "deal_attributes"
                ]
            },
            "name": {
                "type": "string"
            },
            "room_count": {
                "type": "number"
            },
            "transactional_policy_data": {
                "type": "object",
                "properties": {
                "booking_conditions": {
                    "type": "array",
                    "items": {
                    "type": "object",
                    "properties": {
                        "type": {
                        "type": "string"
                        },
                        "description": {
                        "type": "string"
                        },
                        "policy_type_key": {
                        "type": "string"
                        },
                        "key": {
                        "type": "string"
                        },
                        "text": {
                        "type": "string"
                        },
                        "icon": {
                        "type": "string"
                        },
                        "parameters": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                            "key": {
                                "type": "string"
                            },
                            "value": {
                                "type": "string"
                            },
                            "format": {
                                "type": "string"
                            },
                            "type": {
                                "type": "string"
                            }
                            },
                            "required": [
                            "key",
                            "value",
                            "type"
                            ]
                        }
                        },
                        "footer": {
                        "type": "string"
                        }
                    },
                    "required": [
                        "type",
                        "description",
                        "policy_type_key",
                        "key",
                        "text",
                        "icon"
                    ]
                    }
                },
                "policies": {
                    "type": "array",
                    "items": {
                    "type": "object",
                    "properties": {
                        "description": {
                        "type": "string"
                        },
                        "policy_type_key": {
                        "type": "string"
                        },
                        "text": {
                        "type": "string"
                        },
                        "key": {
                        "type": "string"
                        },
                        "parameters": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                            "type": {
                                "type": "string"
                            },
                            "format": {
                                "type": "string"
                            },
                            "value": {
                                "type": "string"
                            },
                            "key": {
                                "type": "string"
                            }
                            },
                            "required": [
                            "type",
                            "value",
                            "key"
                            ]
                        }
                        },
                        "icon": {
                        "type": "string"
                        },
                        "footer": {
                        "type": "string"
                        },
                        "type": {
                        "type": "string"
                        }
                    },
                    "required": [
                        "description",
                        "policy_type_key",
                        "text",
                        "key",
                        "icon",
                        "type"
                    ]
                    }
                }
                },
                "required": [
                "booking_conditions",
                "policies"
                ]
            },
            "policy_display_details": {
                "type": "object",
                "properties": {
                "prepayment": {
                    "type": "object",
                    "properties": {
                    "description_details": {
                        "type": "object",
                        "properties": {
                        "placeholder_translation": {
                            "type": "string"
                        },
                        "translation": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "placeholder_translation",
                        "translation"
                        ]
                    },
                    "type": {
                        "type": "string"
                    },
                    "title_details": {
                        "type": "object",
                        "properties": {
                        "has_html": {
                            "type": "number"
                        },
                        "placeholder_translation": {
                            "type": "string"
                        },
                        "translation": {
                            "type": "string"
                        },
                        "tag": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "has_html",
                        "placeholder_translation",
                        "translation",
                        "tag"
                        ]
                    },
                    "policy_type_key": {
                        "type": "string"
                    }
                    },
                    "required": [
                    "description_details",
                    "type",
                    "title_details",
                    "policy_type_key"
                    ]
                },
                "cancellation": {
                    "type": "object",
                    "properties": {
                    "clarification_details": {
                        "type": "object",
                        "properties": {
                        "tag": {
                            "type": "string"
                        },
                        "translation": {
                            "type": "string"
                        },
                        "placeholder_translation": {
                            "type": "string"
                        },
                        "parameters": {
                            "type": "object",
                            "properties": {
                            "date": {
                                "type": "string"
                            },
                            "timezone": {
                                "type": "string"
                            }
                            },
                            "required": [
                            "date",
                            "timezone"
                            ]
                        }
                        },
                        "required": [
                        "tag",
                        "translation",
                        "placeholder_translation",
                        "parameters"
                        ]
                    },
                    "type": {
                        "type": "string"
                    },
                    "policy_type_key": {
                        "type": "string"
                    },
                    "description_details": {
                        "type": "object",
                        "properties": {
                        "placeholder_translation": {
                            "type": "string"
                        },
                        "translation": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "placeholder_translation",
                        "translation"
                        ]
                    },
                    "title_details": {
                        "type": "object",
                        "properties": {
                        "parameters": {
                            "type": "object",
                            "properties": {
                            "date": {
                                "type": "string"
                            },
                            "timezone": {
                                "type": "string"
                            },
                            "free_cancellation_deadline": {
                                "type": "string"
                            }
                            },
                            "required": [
                            "date",
                            "timezone",
                            "free_cancellation_deadline"
                            ]
                        },
                        "placeholder_translation": {
                            "type": "string"
                        },
                        "has_html": {
                            "type": "number"
                        },
                        "tag": {
                            "type": "string"
                        },
                        "translation": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "parameters",
                        "placeholder_translation",
                        "has_html",
                        "tag",
                        "translation"
                        ]
                    },
                    "parameters": {
                        "type": "object",
                        "properties": {
                        "has_cancellation_fee": {
                            "type": "number"
                        }
                        },
                        "required": [
                        "has_cancellation_fee"
                        ]
                    }
                    },
                    "required": [
                    "clarification_details",
                    "type",
                    "policy_type_key",
                    "description_details",
                    "title_details",
                    "parameters"
                    ]
                }
                },
                "required": [
                "prepayment",
                "cancellation"
                ]
            },
            "pod_ios_migrate_policies_to_smp_fullon": {
                "type": "number"
            },
            "genius_discount_percentage": {
                "type": "number"
            },
            "must_reserve_free_parking": {
                "type": "number"
            },
            "is_mobile_deal": {
                "type": "number"
            },
            "pre_auth_bo_nocc": {
                "type": "number"
            },
            "transactional_policy_objects": {
                "type": "array",
                "items": {
                "type": "object",
                "properties": {
                    "parameters": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                        "key": {
                            "type": "string"
                        },
                        "value": {
                            "type": "string"
                        },
                        "format": {
                            "type": "string"
                        },
                        "type": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "key",
                        "value",
                        "type"
                        ]
                    }
                    },
                    "icon": {
                    "type": "string"
                    },
                    "key": {
                    "type": "string"
                    },
                    "text": {
                    "type": "string"
                    }
                },
                "required": [
                    "icon",
                    "key",
                    "text"
                ]
                }
            },
            "number_of_bathrooms": {
                "type": "number"
            },
            "product_price_breakdown": {
                "type": "object",
                "properties": {
                "price_display_config": {
                    "type": "array",
                    "items": {
                    "type": "object",
                    "properties": {
                        "value": {
                        "type": "number"
                        },
                        "key": {
                        "type": "string"
                        }
                    },
                    "required": [
                        "value",
                        "key"
                    ]
                    }
                },
                "net_amount": {
                    "type": "object",
                    "properties": {
                    "amount_rounded": {
                        "type": "string"
                    },
                    "value": {
                        "type": "number"
                    },
                    "currency": {
                        "type": "string"
                    },
                    "amount_unrounded": {
                        "type": "string"
                    }
                    },
                    "required": [
                    "amount_rounded",
                    "value",
                    "currency",
                    "amount_unrounded"
                    ]
                },
                "has_long_stays_monthly_rate_price": {
                    "type": "number"
                },
                "excluded_amount": {
                    "type": "object",
                    "properties": {
                    "currency": {
                        "type": "string"
                    },
                    "amount_unrounded": {
                        "type": "string"
                    },
                    "amount_rounded": {
                        "type": "string"
                    },
                    "value": {
                        "type": "number"
                    }
                    },
                    "required": [
                    "currency",
                    "amount_unrounded",
                    "amount_rounded",
                    "value"
                    ]
                },
                "strikethrough_amount": {
                    "type": "object",
                    "properties": {
                    "currency": {
                        "type": "string"
                    },
                    "amount_unrounded": {
                        "type": "string"
                    },
                    "value": {
                        "type": "number"
                    },
                    "amount_rounded": {
                        "type": "string"
                    }
                    },
                    "required": [
                    "currency",
                    "amount_unrounded",
                    "value",
                    "amount_rounded"
                    ]
                },
                "gross_amount_per_night": {
                    "type": "object",
                    "properties": {
                    "amount_rounded": {
                        "type": "string"
                    },
                    "value": {
                        "type": "number"
                    },
                    "currency": {
                        "type": "string"
                    },
                    "amount_unrounded": {
                        "type": "string"
                    }
                    },
                    "required": [
                    "amount_rounded",
                    "value",
                    "currency",
                    "amount_unrounded"
                    ]
                },
                "items": {
                    "type": "array",
                    "items": {
                    "type": "object",
                    "properties": {
                        "kind": {
                        "type": "string"
                        },
                        "name": {
                        "type": "string"
                        },
                        "inclusion_type": {
                        "type": "string"
                        },
                        "item_amount": {
                        "type": "object",
                        "properties": {
                            "currency": {
                            "type": "string"
                            },
                            "amount_unrounded": {
                            "type": "string"
                            },
                            "amount_rounded": {
                            "type": "string"
                            },
                            "value": {
                            "type": "number"
                            }
                        },
                        "required": [
                            "currency",
                            "amount_unrounded",
                            "amount_rounded",
                            "value"
                        ]
                        },
                        "details": {
                        "type": "string"
                        },
                        "base": {
                        "type": "object",
                        "properties": {
                            "kind": {
                            "type": "string"
                            },
                            "percentage": {
                            "type": "number"
                            }
                        },
                        "required": [
                            "kind"
                        ]
                        },
                        "identifier": {
                        "type": "string"
                        }
                    },
                    "required": [
                        "kind",
                        "name",
                        "item_amount",
                        "details",
                        "base"
                    ]
                    }
                },
                "strikethrough_amount_per_night": {
                    "type": "object",
                    "properties": {
                    "value": {
                        "type": "number"
                    },
                    "amount_rounded": {
                        "type": "string"
                    },
                    "currency": {
                        "type": "string"
                    },
                    "amount_unrounded": {
                        "type": "string"
                    }
                    },
                    "required": [
                    "value",
                    "amount_rounded",
                    "currency",
                    "amount_unrounded"
                    ]
                },
                "gross_amount_hotel_currency": {
                    "type": "object",
                    "properties": {
                    "amount_unrounded": {
                        "type": "string"
                    },
                    "currency": {
                        "type": "string"
                    },
                    "amount_rounded": {
                        "type": "string"
                    },
                    "value": {
                        "type": "number"
                    }
                    },
                    "required": [
                    "amount_unrounded",
                    "currency",
                    "amount_rounded",
                    "value"
                    ]
                },
                "included_taxes_and_charges_amount": {
                    "type": "object",
                    "properties": {
                    "amount_rounded": {
                        "type": "string"
                    },
                    "value": {
                        "type": "number"
                    },
                    "amount_unrounded": {
                        "type": "string"
                    },
                    "currency": {
                        "type": "string"
                    }
                    },
                    "required": [
                    "amount_rounded",
                    "value",
                    "amount_unrounded",
                    "currency"
                    ]
                },
                "charges_details": {
                    "type": "object",
                    "properties": {
                    "amount": {
                        "type": "object",
                        "properties": {
                        "value": {
                            "type": "number"
                        },
                        "currency": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "value",
                        "currency"
                        ]
                    },
                    "mode": {
                        "type": "string"
                    }
                    },
                    "required": [
                    "amount",
                    "mode"
                    ]
                },
                "client_translations": {
                    "type": "object",
                    "properties": {
                    "tooltip_total_text": {
                        "type": "string"
                    }
                    },
                    "required": [
                    "tooltip_total_text"
                    ]
                },
                "all_inclusive_amount": {
                    "type": "object",
                    "properties": {
                    "value": {
                        "type": "number"
                    },
                    "amount_rounded": {
                        "type": "string"
                    },
                    "amount_unrounded": {
                        "type": "string"
                    },
                    "currency": {
                        "type": "string"
                    }
                    },
                    "required": [
                    "value",
                    "amount_rounded",
                    "amount_unrounded",
                    "currency"
                    ]
                },
                "has_long_stays_weekly_rate_price": {
                    "type": "number"
                },
                "benefits": {
                    "type": "array",
                    "items": {
                    "type": "object",
                    "properties": {
                        "badge_variant": {
                        "type": "string"
                        },
                        "identifier": {
                        "type": "string"
                        },
                        "details": {
                        "type": "string"
                        },
                        "kind": {
                        "type": "string"
                        },
                        "name": {
                        "type": "string"
                        }
                    },
                    "required": [
                        "badge_variant",
                        "identifier",
                        "details",
                        "kind",
                        "name"
                    ]
                    }
                },
                "gross_amount": {
                    "type": "object",
                    "properties": {
                    "currency": {
                        "type": "string"
                    },
                    "amount_unrounded": {
                        "type": "string"
                    },
                    "value": {
                        "type": "number"
                    },
                    "amount_rounded": {
                        "type": "string"
                    }
                    },
                    "required": [
                    "currency",
                    "amount_unrounded",
                    "value",
                    "amount_rounded"
                    ]
                },
                "discounted_amount": {
                    "type": "object",
                    "properties": {
                    "value": {
                        "type": "number"
                    },
                    "amount_rounded": {
                        "type": "string"
                    },
                    "amount_unrounded": {
                        "type": "string"
                    },
                    "currency": {
                        "type": "string"
                    }
                    },
                    "required": [
                    "value",
                    "amount_rounded",
                    "amount_unrounded",
                    "currency"
                    ]
                },
                "nr_stays": {
                    "type": "number"
                },
                "all_inclusive_amount_hotel_currency": {
                    "type": "object",
                    "properties": {
                    "amount_rounded": {
                        "type": "string"
                    },
                    "value": {
                        "type": "number"
                    },
                    "currency": {
                        "type": "string"
                    },
                    "amount_unrounded": {
                        "type": "string"
                    }
                    },
                    "required": [
                    "amount_rounded",
                    "value",
                    "currency",
                    "amount_unrounded"
                    ]
                }
                },
                "required": [
                "price_display_config",
                "net_amount",
                "has_long_stays_monthly_rate_price",
                "excluded_amount",
                "gross_amount_per_night",
                "items",
                "gross_amount_hotel_currency",
                "included_taxes_and_charges_amount",
                "charges_details",
                "client_translations",
                "all_inclusive_amount",
                "has_long_stays_weekly_rate_price",
                "gross_amount",
                "nr_stays",
                "all_inclusive_amount_hotel_currency"
                ]
            },
            "is_dormitory": {
                "type": "number"
            },
            "paymentterms": {
                "type": "object",
                "properties": {
                "cancellation": {
                    "type": "object",
                    "properties": {
                    "timeline": {
                        "type": "object",
                        "properties": {
                        "nr_stages": {
                            "type": "number"
                        },
                        "stages": {
                            "type": "array",
                            "items": {
                            "type": "object",
                            "properties": {
                                "u_stage_fee_pretty": {
                                "type": "string"
                                },
                                "fee_remaining_pretty": {
                                "type": "string"
                                },
                                "limit_timezone": {
                                "type": "string"
                                },
                                "u_fee_remaining_pretty": {
                                "type": "string"
                                },
                                "u_fee": {
                                "type": "string"
                                },
                                "limit_from_raw": {
                                "type": "string"
                                },
                                "current_stage": {
                                "type": "number"
                                },
                                "is_effective": {
                                "type": "number"
                                },
                                "u_fee_pretty": {
                                "type": "string"
                                },
                                "is_free": {
                                "type": "number"
                                },
                                "stage_fee_pretty": {
                                "type": "string"
                                },
                                "date_until": {
                                "type": "string"
                                },
                                "limit_from": {
                                "type": "string"
                                },
                                "stage_translation": {
                                "type": "string"
                                },
                                "limit_until_date": {
                                "type": "string"
                                },
                                "stage_fee": {
                                "type": "number"
                                },
                                "fee": {
                                "type": "number"
                                },
                                "u_fee_remaining": {
                                "type": "string"
                                },
                                "fee_pretty": {
                                "type": "string"
                                },
                                "u_stage_fee": {
                                "type": "string"
                                },
                                "limit_from_time": {
                                "type": "string"
                                },
                                "limit_until_time": {
                                "type": "string"
                                },
                                "limit_until": {
                                "type": "string"
                                },
                                "limit_from_date": {
                                "type": "string"
                                },
                                "effective_number": {
                                "type": "number"
                                },
                                "text_refundable": {
                                "type": "string"
                                },
                                "fee_rounded": {
                                "type": "number"
                                },
                                "b_number": {
                                "type": "number"
                                },
                                "limit_until_raw": {
                                "type": "string"
                                },
                                "b_state": {
                                "type": "string"
                                },
                                "text": {
                                "type": "string"
                                },
                                "fee_remaining": {
                                "type": "number"
                                },
                                "amount": {},
                                "amount_pretty": {
                                "type": "string"
                                },
                                "date_from": {
                                "type": "string"
                                }
                            },
                            "required": [
                                "u_stage_fee_pretty",
                                "fee_remaining_pretty",
                                "limit_timezone",
                                "u_fee_remaining_pretty",
                                "u_fee",
                                "limit_from_raw",
                                "current_stage",
                                "is_effective",
                                "u_fee_pretty",
                                "is_free",
                                "stage_fee_pretty",
                                "limit_from",
                                "stage_translation",
                                "limit_until_date",
                                "stage_fee",
                                "fee",
                                "u_fee_remaining",
                                "fee_pretty",
                                "u_stage_fee",
                                "limit_from_time",
                                "limit_until_time",
                                "limit_until",
                                "limit_from_date",
                                "effective_number",
                                "text_refundable",
                                "fee_rounded",
                                "b_number",
                                "limit_until_raw",
                                "b_state",
                                "text",
                                "fee_remaining",
                                "amount"
                            ]
                            }
                        },
                        "u_currency_code": {
                            "type": "string"
                        },
                        "currency_code": {
                            "type": "string"
                        },
                        "policygroup_instance_id": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "nr_stages",
                        "stages",
                        "u_currency_code",
                        "currency_code",
                        "policygroup_instance_id"
                        ]
                    },
                    "type": {
                        "type": "string"
                    },
                    "info": {
                        "type": "object",
                        "properties": {
                        "time": {
                            "type": "string"
                        },
                        "refundable_date_midnight": {
                            "type": "string"
                        },
                        "refundable": {
                            "type": "number"
                        },
                        "date": {
                            "type": "string"
                        },
                        "timezone_offset": {
                            "type": "string"
                        },
                        "date_raw": {
                            "type": "string"
                        },
                        "date_before": {
                            "type": "string"
                        },
                        "is_midnight": {
                            "type": "number"
                        },
                        "date_before_raw": {
                            "type": "string"
                        },
                        "time_before_midnight": {
                            "type": "string"
                        },
                        "refundable_date": {
                            "type": "string"
                        },
                        "timezone": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "time",
                        "refundable_date_midnight",
                        "refundable",
                        "date",
                        "timezone_offset",
                        "date_raw",
                        "date_before",
                        "is_midnight",
                        "date_before_raw",
                        "time_before_midnight",
                        "refundable_date",
                        "timezone"
                        ]
                    },
                    "description": {
                        "type": "string"
                    },
                    "type_translation": {
                        "type": "string"
                    },
                    "non_refundable_anymore": {
                        "type": "number"
                    },
                    "guaranteed_non_refundable": {
                        "type": "number"
                    },
                    "bucket": {
                        "type": "string"
                    }
                    },
                    "required": [
                    "timeline",
                    "type",
                    "info",
                    "description",
                    "type_translation",
                    "non_refundable_anymore",
                    "guaranteed_non_refundable",
                    "bucket"
                    ]
                },
                "prepayment": {
                    "type": "object",
                    "properties": {
                    "type_translation": {
                        "type": "string"
                    },
                    "description": {
                        "type": "string"
                    },
                    "info": {
                        "type": "object",
                        "properties": {
                        "refundable": {
                            "type": "string"
                        },
                        "prepayment_at_booktime": {
                            "type": "number"
                        }
                        },
                        "required": [
                        "refundable",
                        "prepayment_at_booktime"
                        ]
                    },
                    "simple_translation": {
                        "type": "string"
                    },
                    "type_extended": {
                        "type": "string"
                    },
                    "timeline": {
                        "type": "object",
                        "properties": {
                        "nr_stages": {
                            "type": "number"
                        },
                        "policygroup_instance_id": {
                            "type": "string"
                        },
                        "currency_code": {
                            "type": "string"
                        },
                        "u_currency_code": {
                            "type": "string"
                        },
                        "stages": {
                            "type": "array",
                            "items": {
                            "type": "object",
                            "properties": {
                                "fee_remaining_pretty": {
                                "type": "string"
                                },
                                "limit_timezone": {
                                "type": "string"
                                },
                                "u_stage_fee_pretty": {
                                "type": "string"
                                },
                                "u_fee": {
                                "type": "string"
                                },
                                "limit_from_raw": {
                                "type": "string"
                                },
                                "current_stage": {
                                "type": "number"
                                },
                                "is_effective": {
                                "type": "number"
                                },
                                "u_fee_remaining_pretty": {
                                "type": "string"
                                },
                                "limit_from": {
                                "type": "string"
                                },
                                "amount_pretty": {
                                "type": "string"
                                },
                                "u_fee_pretty": {
                                "type": "string"
                                },
                                "is_free": {
                                "type": "number"
                                },
                                "stage_fee_pretty": {
                                "type": "string"
                                },
                                "stage_fee": {
                                "type": "number"
                                },
                                "amount": {
                                "type": "string"
                                },
                                "fee": {
                                "type": "number"
                                },
                                "limit_until_date": {
                                "type": "string"
                                },
                                "limit_from_time": {
                                "type": "string"
                                },
                                "limit_until": {
                                "type": "string"
                                },
                                "limit_until_time": {
                                "type": "string"
                                },
                                "limit_from_date": {
                                "type": "string"
                                },
                                "u_fee_remaining": {
                                "type": "string"
                                },
                                "fee_pretty": {
                                "type": "string"
                                },
                                "u_stage_fee": {
                                "type": "string"
                                },
                                "fee_rounded": {
                                "type": "number"
                                },
                                "b_number": {
                                "type": "number"
                                },
                                "effective_number": {
                                "type": "number"
                                },
                                "b_state": {
                                "type": "string"
                                },
                                "text": {
                                "type": "string"
                                },
                                "fee_remaining": {
                                "type": "number"
                                },
                                "limit_until_raw": {
                                "type": "string"
                                },
                                "after_checkin": {
                                "type": "number"
                                }
                            },
                            "required": [
                                "amount_pretty",
                                "is_free",
                                "amount",
                                "text"
                            ]
                            }
                        }
                        },
                        "required": [
                        "nr_stages",
                        "policygroup_instance_id",
                        "currency_code",
                        "u_currency_code",
                        "stages"
                        ]
                    },
                    "extended_type_translation": {
                        "type": "string"
                    },
                    "type": {
                        "type": "string"
                    }
                    },
                    "required": [
                    "type_translation",
                    "description",
                    "info",
                    "simple_translation",
                    "type_extended",
                    "timeline",
                    "extended_type_translation",
                    "type"
                    ]
                }
                },
                "required": [
                "cancellation",
                "prepayment"
                ]
            },
            "is_last_minute_deal": {
                "type": "number"
            },
            "room_name": {
                "type": "string"
            },
            "is_block_fit": {
                "type": "number"
            },
            "extrabed_available": {
                "type": "number"
            },
            "room_surface_in_feet2": {
                "type": "number"
            },
            "babycots_available": {
                "type": "number"
            },
            "room_id": {
                "type": "number"
            },
            "is_temp_charge_enabled": {
                "type": "number"
            },
            "can_reserve_free_parking": {
                "type": "number"
            },
            "deposit_required": {
                "type": "number"
            },
            "roomtype_id": {
                "type": "number"
            },
            "all_inclusive": {
                "type": "number"
            },
            "is_domestic_rate": {
                "type": "number"
            },
            "is_secret_deal": {
                "type": "number"
            },
            "is_flash_deal": {
                "type": "number"
            },
            "mealplan": {
                "type": "string"
            },
            "nr_adults": {
                "type": "number"
            },
            "room_surface_in_m2": {
                "type": "number"
            },
            "block_text": {
                "type": "object",
                "properties": {
                "policies": {
                    "type": "array",
                    "items": {
                    "type": "object",
                    "properties": {
                        "content": {
                        "type": "string"
                        },
                        "class": {
                        "type": "string"
                        },
                        "mealplan_vector": {
                        "type": "string"
                        }
                    },
                    "required": [
                        "content",
                        "class"
                    ]
                    }
                }
                },
                "required": [
                "policies"
                ]
            },
            "max_children_free": {
                "type": "number"
            },
            "smoking": {
                "type": "number"
            },
            "is_smart_deal": {
                "type": "number"
            },
            "number_of_bedrooms": {
                "type": "number"
            },
            "half_board": {
                "type": "number"
            },
            "refundable": {
                "type": "number"
            },
            "refundable_until": {
                "type": "string"
            },
            "breakfast_included": {
                "type": "number"
            },
            "max_occupancy": {
                "type": "number"
            },
            "block_id": {
                "type": "string"
            }
            },
            "required": [
            "name_without_policy",
            "nr_children",
            "max_children_free_age",
            "package_id",
            "full_board",
            "deals",
            "name",
            "room_count",
            "transactional_policy_data",
            "policy_display_details",
            "pod_ios_migrate_policies_to_smp_fullon",
            "genius_discount_percentage",
            "must_reserve_free_parking",
            "is_mobile_deal",
            "pre_auth_bo_nocc",
            "transactional_policy_objects",
            "number_of_bathrooms",
            "product_price_breakdown",
            "is_dormitory",
            "paymentterms",
            "is_last_minute_deal",
            "room_name",
            "is_block_fit",
            "extrabed_available",
            "room_surface_in_feet2",
            "babycots_available",
            "room_id",
            "is_temp_charge_enabled",
            "can_reserve_free_parking",
            "deposit_required",
            "roomtype_id",
            "all_inclusive",
            "is_domestic_rate",
            "is_secret_deal",
            "is_flash_deal",
            "mealplan",
            "nr_adults",
            "room_surface_in_m2",
            "block_text",
            "max_children_free",
            "smoking",
            "is_smart_deal",
            "number_of_bedrooms",
            "half_board",
            "refundable",
            "refundable_until",
            "breakfast_included",
            "max_occupancy",
            "block_id"
            ]
        }
        },
        "unavailable": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
            "block_id": {
                "type": "string"
            },
            "number_of_bedrooms": {
                "type": "number"
            },
            "smoking": {
                "type": "number"
            },
            "package_id": {
                "type": "number"
            },
            "is_temp_charge_enabled": {
                "type": "number"
            },
            "name_without_policy": {
                "type": "string"
            },
            "room_surface_in_feet2": {
                "type": "number"
            },
            "refundable": {
                "type": "number"
            },
            "nr_children": {
                "type": "number"
            },
            "transactional_policy_data": {
                "type": "object",
                "properties": {
                "policies": {
                    "type": "array",
                    "items": {
                    "type": "object",
                    "properties": {
                        "type": {
                        "type": "string"
                        },
                        "text": {
                        "type": "string"
                        },
                        "description": {
                        "type": "string"
                        },
                        "icon": {
                        "type": "string"
                        },
                        "policy_type_key": {
                        "type": "string"
                        },
                        "parameters": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                            "value": {
                                "type": "string"
                            },
                            "key": {
                                "type": "string"
                            },
                            "format": {
                                "type": "string"
                            },
                            "type": {
                                "type": "string"
                            }
                            },
                            "required": [
                            "value",
                            "key",
                            "type"
                            ]
                        }
                        },
                        "key": {
                        "type": "string"
                        },
                        "footer": {
                        "type": "string"
                        }
                    },
                    "required": [
                        "type",
                        "text",
                        "description",
                        "icon",
                        "policy_type_key",
                        "key"
                    ]
                    }
                },
                "booking_conditions": {
                    "type": "array",
                    "items": {
                    "type": "object",
                    "properties": {
                        "icon": {
                        "type": "string"
                        },
                        "type": {
                        "type": "string"
                        },
                        "description": {
                        "type": "string"
                        },
                        "text": {
                        "type": "string"
                        },
                        "key": {
                        "type": "string"
                        },
                        "policy_type_key": {
                        "type": "string"
                        },
                        "parameters": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                            "type": {
                                "type": "string"
                            },
                            "format": {
                                "type": "string"
                            },
                            "value": {
                                "type": "string"
                            },
                            "key": {
                                "type": "string"
                            }
                            },
                            "required": [
                            "type",
                            "value",
                            "key"
                            ]
                        }
                        },
                        "footer": {
                        "type": "string"
                        }
                    },
                    "required": [
                        "icon",
                        "type",
                        "description",
                        "text",
                        "key",
                        "policy_type_key"
                    ]
                    }
                }
                },
                "required": [
                "policies",
                "booking_conditions"
                ]
            },
            "max_occupancy": {
                "type": "number"
            },
            "nr_adults": {
                "type": "number"
            },
            "is_dormitory": {
                "type": "number"
            },
            "babycots_available": {
                "type": "number"
            },
            "extrabed_available": {
                "type": "number"
            },
            "half_board": {
                "type": "number"
            },
            "is_mobile_deal": {
                "type": "number"
            },
            "room_id": {
                "type": "number"
            },
            "room_surface_in_m2": {
                "type": "number"
            },
            "breakfast_included": {
                "type": "number"
            },
            "full_board": {
                "type": "number"
            },
            "room_name": {
                "type": "string"
            },
            "is_domestic_rate": {
                "type": "number"
            },
            "name": {
                "type": "string"
            },
            "is_flash_deal": {
                "type": "number"
            },
            "deposit_required": {
                "type": "number"
            },
            "policy_display_details": {
                "type": "object",
                "properties": {
                "cancellation": {
                    "type": "object",
                    "properties": {
                    "title_details": {
                        "type": "object",
                        "properties": {
                        "parameters": {
                            "type": "object",
                            "properties": {
                            "date": {
                                "type": "string"
                            },
                            "free_cancellation_deadline": {
                                "type": "string"
                            },
                            "timezone": {
                                "type": "string"
                            }
                            },
                            "required": [
                            "date",
                            "free_cancellation_deadline",
                            "timezone"
                            ]
                        },
                        "has_html": {
                            "type": "number"
                        },
                        "placeholder_translation": {
                            "type": "string"
                        },
                        "tag": {
                            "type": "string"
                        },
                        "translation": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "parameters",
                        "has_html",
                        "placeholder_translation",
                        "tag",
                        "translation"
                        ]
                    },
                    "parameters": {
                        "type": "object",
                        "properties": {
                        "has_cancellation_fee": {
                            "type": "number"
                        }
                        },
                        "required": [
                        "has_cancellation_fee"
                        ]
                    },
                    "policy_type_key": {
                        "type": "string"
                    },
                    "description_details": {
                        "type": "object",
                        "properties": {
                        "placeholder_translation": {
                            "type": "string"
                        },
                        "translation": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "placeholder_translation",
                        "translation"
                        ]
                    },
                    "clarification_details": {
                        "type": "object",
                        "properties": {
                        "parameters": {
                            "type": "object",
                            "properties": {
                            "timezone": {
                                "type": "string"
                            },
                            "date": {
                                "type": "string"
                            }
                            },
                            "required": [
                            "timezone",
                            "date"
                            ]
                        },
                        "placeholder_translation": {
                            "type": "string"
                        },
                        "tag": {
                            "type": "string"
                        },
                        "translation": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "parameters",
                        "placeholder_translation",
                        "tag",
                        "translation"
                        ]
                    },
                    "type": {
                        "type": "string"
                    }
                    },
                    "required": [
                    "title_details",
                    "parameters",
                    "policy_type_key",
                    "description_details",
                    "clarification_details",
                    "type"
                    ]
                },
                "prepayment": {
                    "type": "object",
                    "properties": {
                    "description_details": {
                        "type": "object",
                        "properties": {
                        "translation": {
                            "type": "string"
                        },
                        "placeholder_translation": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "translation",
                        "placeholder_translation"
                        ]
                    },
                    "type": {
                        "type": "string"
                    },
                    "title_details": {
                        "type": "object",
                        "properties": {
                        "placeholder_translation": {
                            "type": "string"
                        },
                        "tag": {
                            "type": "string"
                        },
                        "has_html": {
                            "type": "number"
                        },
                        "translation": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "placeholder_translation",
                        "tag",
                        "has_html",
                        "translation"
                        ]
                    },
                    "policy_type_key": {
                        "type": "string"
                    }
                    },
                    "required": [
                    "description_details",
                    "type",
                    "title_details",
                    "policy_type_key"
                    ]
                }
                },
                "required": [
                "cancellation",
                "prepayment"
                ]
            },
            "room_count": {
                "type": "number"
            },
            "max_children_free_age": {
                "type": "number"
            },
            "pre_auth_bo_nocc": {
                "type": "number"
            },
            "can_reserve_free_parking": {
                "type": "number"
            },
            "number_of_bathrooms": {
                "type": "number"
            },
            "max_children_free": {
                "type": "number"
            },
            "roomtype_id": {
                "type": "number"
            },
            "block_text": {
                "type": "object",
                "properties": {
                "policies": {
                    "type": "array",
                    "items": {
                    "type": "object",
                    "properties": {
                        "content": {
                        "type": "string"
                        },
                        "class": {
                        "type": "string"
                        },
                        "mealplan_vector": {
                        "type": "string"
                        }
                    },
                    "required": [
                        "content",
                        "class"
                    ]
                    }
                }
                },
                "required": [
                "policies"
                ]
            },
            "must_reserve_free_parking": {
                "type": "number"
            },
            "is_block_fit": {
                "type": "number"
            },
            "all_inclusive": {
                "type": "number"
            },
            "mealplan": {
                "type": "string"
            }
            },
            "required": [
            "block_id",
            "number_of_bedrooms",
            "smoking",
            "package_id",
            "is_temp_charge_enabled",
            "name_without_policy",
            "room_surface_in_feet2",
            "refundable",
            "nr_children",
            "transactional_policy_data",
            "max_occupancy",
            "nr_adults",
            "is_dormitory",
            "babycots_available",
            "extrabed_available",
            "half_board",
            "is_mobile_deal",
            "room_id",
            "room_surface_in_m2",
            "breakfast_included",
            "full_board",
            "room_name",
            "is_domestic_rate",
            "name",
            "is_flash_deal",
            "deposit_required",
            "policy_display_details",
            "room_count",
            "max_children_free_age",
            "pre_auth_bo_nocc",
            "can_reserve_free_parking",
            "number_of_bathrooms",
            "max_children_free",
            "roomtype_id",
            "block_text",
            "must_reserve_free_parking",
            "is_block_fit",
            "all_inclusive",
            "mealplan"
            ]
        }
        }
    },
    "required": [
        "status",
        "available",
        "unavailable"
    ]
    }    
    """
    def __init__(self, api_response_fpath: str) -> None:
        super().__init__(api_response_fpath)

    def init_task_list(self) -> list[Type[base.Task]]:
        task_list = [
            booking_rooms_with_availability.GetRoomCount,
            booking_rooms_with_availability.GetRoomArea,
            booking_rooms_with_availability.GetRoomsWithPriceLessThanAmount,
            booking_rooms_with_availability.GetRoomsWithMealPlan,
            booking_rooms_with_availability.GetLowestCost,
            booking_rooms_with_availability.GetHighestVAT,
        ]

        return task_list


class BookingSearchHotelByCoordinatesTaskList(TaskList):

    response_json_schema: str = """
    {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Response schema for the search hotels by coordinates endpoint.",
    "type": "object",
    "properties": {
        "status": {
        "type": "boolean"
        },
        "message": {
        "type": "string"
        },
        "data": {
        "type": "object",
        "properties": {
            "count": {
            "type": "number"
            },
            "primary_count": {
            "type": "number"
            },
            "extended_count": {
            "type": "number"
            },
            "page_loading_threshold": {
            "type": "number"
            },
            "filters": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                "title": {
                    "type": "string"
                },
                "field": {
                    "type": "string"
                }
                },
                "required": [
                "title",
                "field"
                ]
            }
            },
            "result": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                "hotel_id": {
                    "type": "number"
                },
                "preferred_plus": {
                    "type": "number"
                },
                "class_is_estimated": {
                    "type": "number"
                },
                "block_ids": {
                    "type": "array",
                    "items": {
                    "type": "string"
                    }
                },
                "accommodation_type": {
                    "type": "number"
                },
                "longitude": {
                    "type": "number"
                },
                "latitude": {
                    "type": "number"
                },
                "checkout": {
                    "type": "object",
                    "properties": {
                    "until": {
                        "type": "string"
                    },
                    "from": {
                        "type": "string"
                    }
                    },
                    "required": [
                    "until"
                    ]
                },
                "min_total_price": {
                    "type": "number"
                },
                "is_smart_deal": {
                    "type": "number"
                },
                "city_in_trans": {
                    "type": "string"
                },
                "is_tpi_exclusive_property": {
                    "type": "number"
                },
                "timezone": {
                    "type": "string"
                },
                "unit_configuration_label": {
                    "type": "string"
                },
                "urgency_message": {
                    "type": "string"
                },
                "review_score": {
                    "type": "number"
                },
                "class": {
                    "type": "number"
                },
                "badges": {
                    "type": "array",
                    "items": {
                    "type": "object",
                    "properties": {
                        "text": {
                        "type": "string"
                        },
                        "badge_variant": {
                        "type": "string"
                        },
                        "id": {
                        "type": "string"
                        }
                    },
                    "required": [
                        "text",
                        "badge_variant",
                        "id"
                    ]
                    }
                },
                "last_reservation_data": {
                    "type": "object",
                    "properties": {
                    "last_reservation_ellapsed_months": {
                        "type": "number"
                    }
                    },
                    "required": [
                    "last_reservation_ellapsed_months"
                    ]
                },
                "extended": {
                    "type": "number"
                },
                "checkin": {
                    "type": "object",
                    "properties": {
                    "from": {
                        "type": "string"
                    },
                    "until": {
                        "type": "string"
                    }
                    },
                    "required": [
                    "from"
                    ]
                },
                "soldout": {
                    "type": "number"
                },
                "hotel_has_vb_boost": {
                    "type": "number"
                },
                "type": {
                    "type": "string"
                },
                "is_genius_deal": {
                    "type": "number"
                },
                "has_swimming_pool": {
                    "type": "number"
                },
                "is_no_prepayment_block": {
                    "type": "number"
                },
                "bwallet": {
                    "type": "object",
                    "properties": {
                    "hotel_eligibility": {
                        "type": "number"
                    }
                    },
                    "required": [
                    "hotel_eligibility"
                    ]
                },
                "default_wishlist_name": {
                    "type": "string"
                },
                "ufi": {
                    "type": "number"
                },
                "is_free_cancellable": {
                    "type": "number"
                },
                "preferred": {
                    "type": "number"
                },
                "main_photo_id": {
                    "type": "number"
                },
                "default_language": {
                    "type": "string"
                },
                "review_score_word": {
                    "type": "string"
                },
                "booking_home": {
                    "type": "object",
                    "properties": {
                    "group": {
                        "type": "string"
                    },
                    "segment": {
                        "type": "number"
                    },
                    "is_single_unit_property": {
                        "type": "number"
                    },
                    "is_booking_home": {
                        "type": "number"
                    },
                    "quality_class": {
                        "type": "number"
                    }
                    },
                    "required": [
                    "group",
                    "segment",
                    "is_single_unit_property",
                    "is_booking_home",
                    "quality_class"
                    ]
                },
                "genius_discount_percentage": {
                    "type": "number"
                },
                "hotel_name_trans": {
                    "type": "string"
                },
                "city": {
                    "type": "string"
                },
                "hotel_include_breakfast": {
                    "type": "number"
                },
                "composite_price_breakdown": {
                    "type": "object",
                    "properties": {
                    "price_display_config": {
                        "type": "array",
                        "items": {
                        "type": "object",
                        "properties": {
                            "value": {
                            "type": "number"
                            },
                            "key": {
                            "type": "string"
                            }
                        },
                        "required": [
                            "value",
                            "key"
                        ]
                        }
                    },
                    "all_inclusive_amount": {
                        "type": "object",
                        "properties": {
                        "amount_rounded": {
                            "type": "string"
                        },
                        "value": {
                            "type": "number"
                        },
                        "amount_unrounded": {
                            "type": "string"
                        },
                        "currency": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "amount_rounded",
                        "value",
                        "amount_unrounded",
                        "currency"
                        ]
                    },
                    "client_translations": {
                        "type": "object",
                        "properties": {
                        "tooltip_total_text": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "tooltip_total_text"
                        ]
                    },
                    "benefits": {
                        "type": "array",
                        "items": {
                        "type": "object",
                        "properties": {
                            "kind": {
                            "type": "string"
                            },
                            "name": {
                            "type": "string"
                            },
                            "identifier": {
                            "type": "string"
                            },
                            "details": {
                            "type": "string"
                            },
                            "badge_variant": {
                            "type": "string"
                            }
                        },
                        "required": [
                            "kind",
                            "name",
                            "identifier",
                            "details",
                            "badge_variant"
                        ]
                        }
                    },
                    "has_long_stays_weekly_rate_price": {
                        "type": "number"
                    },
                    "excluded_amount": {
                        "type": "object",
                        "properties": {
                        "currency": {
                            "type": "string"
                        },
                        "value": {
                            "type": "number"
                        },
                        "amount_unrounded": {
                            "type": "string"
                        },
                        "amount_rounded": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "currency",
                        "value",
                        "amount_unrounded",
                        "amount_rounded"
                        ]
                    },
                    "gross_amount_per_night": {
                        "type": "object",
                        "properties": {
                        "currency": {
                            "type": "string"
                        },
                        "value": {
                            "type": "number"
                        },
                        "amount_unrounded": {
                            "type": "string"
                        },
                        "amount_rounded": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "currency",
                        "value",
                        "amount_unrounded",
                        "amount_rounded"
                        ]
                    },
                    "net_amount": {
                        "type": "object",
                        "properties": {
                        "currency": {
                            "type": "string"
                        },
                        "amount_unrounded": {
                            "type": "string"
                        },
                        "value": {
                            "type": "number"
                        },
                        "amount_rounded": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "currency",
                        "amount_unrounded",
                        "value",
                        "amount_rounded"
                        ]
                    },
                    "discounted_amount": {
                        "type": "object",
                        "properties": {
                        "currency": {
                            "type": "string"
                        },
                        "value": {
                            "type": "number"
                        },
                        "amount_unrounded": {
                            "type": "string"
                        },
                        "amount_rounded": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "currency",
                        "value",
                        "amount_unrounded",
                        "amount_rounded"
                        ]
                    },
                    "included_taxes_and_charges_amount": {
                        "type": "object",
                        "properties": {
                        "amount_unrounded": {
                            "type": "string"
                        },
                        "value": {
                            "type": "number"
                        },
                        "currency": {
                            "type": "string"
                        },
                        "amount_rounded": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "amount_unrounded",
                        "value",
                        "currency",
                        "amount_rounded"
                        ]
                    },
                    "items": {
                        "type": "array",
                        "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                            "type": "string"
                            },
                            "item_amount": {
                            "type": "object",
                            "properties": {
                                "currency": {
                                "type": "string"
                                },
                                "amount_unrounded": {
                                "type": "string"
                                },
                                "value": {
                                "type": "number"
                                },
                                "amount_rounded": {
                                "type": "string"
                                }
                            },
                            "required": [
                                "currency",
                                "amount_unrounded",
                                "value",
                                "amount_rounded"
                            ]
                            },
                            "base": {
                            "type": "object",
                            "properties": {
                                "kind": {
                                "type": "string"
                                },
                                "percentage": {
                                "type": "number"
                                },
                                "base_amount": {
                                "type": "number"
                                }
                            },
                            "required": [
                                "kind"
                            ]
                            },
                            "details": {
                            "type": "string"
                            },
                            "kind": {
                            "type": "string"
                            },
                            "inclusion_type": {
                            "type": "string"
                            },
                            "identifier": {
                            "type": "string"
                            }
                        },
                        "required": [
                            "name",
                            "item_amount",
                            "base",
                            "kind"
                        ]
                        }
                    },
                    "strikethrough_amount_per_night": {
                        "type": "object",
                        "properties": {
                        "value": {
                            "type": "number"
                        },
                        "amount_unrounded": {
                            "type": "string"
                        },
                        "currency": {
                            "type": "string"
                        },
                        "amount_rounded": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "value",
                        "amount_unrounded",
                        "currency",
                        "amount_rounded"
                        ]
                    },
                    "strikethrough_amount": {
                        "type": "object",
                        "properties": {
                        "amount_unrounded": {
                            "type": "string"
                        },
                        "value": {
                            "type": "number"
                        },
                        "currency": {
                            "type": "string"
                        },
                        "amount_rounded": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "amount_unrounded",
                        "value",
                        "currency",
                        "amount_rounded"
                        ]
                    },
                    "gross_amount_hotel_currency": {
                        "type": "object",
                        "properties": {
                        "amount_unrounded": {
                            "type": "string"
                        },
                        "value": {
                            "type": "number"
                        },
                        "currency": {
                            "type": "string"
                        },
                        "amount_rounded": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "amount_unrounded",
                        "value",
                        "currency",
                        "amount_rounded"
                        ]
                    },
                    "gross_amount": {
                        "type": "object",
                        "properties": {
                        "amount_rounded": {
                            "type": "string"
                        },
                        "currency": {
                            "type": "string"
                        },
                        "amount_unrounded": {
                            "type": "string"
                        },
                        "value": {
                            "type": "number"
                        }
                        },
                        "required": [
                        "amount_rounded",
                        "currency",
                        "amount_unrounded",
                        "value"
                        ]
                    },
                    "charges_details": {
                        "type": "object",
                        "properties": {
                        "amount": {
                            "type": "object",
                            "properties": {
                            "currency": {
                                "type": "string"
                            },
                            "value": {
                                "type": "number"
                            }
                            },
                            "required": [
                            "currency",
                            "value"
                            ]
                        },
                        "mode": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "amount",
                        "mode"
                        ]
                    },
                    "all_inclusive_amount_hotel_currency": {
                        "type": "object",
                        "properties": {
                        "amount_rounded": {
                            "type": "string"
                        },
                        "currency": {
                            "type": "string"
                        },
                        "amount_unrounded": {
                            "type": "string"
                        },
                        "value": {
                            "type": "number"
                        }
                        },
                        "required": [
                        "amount_rounded",
                        "currency",
                        "amount_unrounded",
                        "value"
                        ]
                    },
                    "has_long_stays_monthly_rate_price": {
                        "type": "number"
                    }
                    },
                    "required": [
                    "price_display_config",
                    "all_inclusive_amount",
                    "client_translations",
                    "benefits",
                    "has_long_stays_weekly_rate_price",
                    "excluded_amount",
                    "gross_amount_per_night",
                    "net_amount",
                    "discounted_amount",
                    "included_taxes_and_charges_amount",
                    "items",
                    "strikethrough_amount_per_night",
                    "strikethrough_amount",
                    "gross_amount_hotel_currency",
                    "gross_amount",
                    "charges_details",
                    "all_inclusive_amount_hotel_currency",
                    "has_long_stays_monthly_rate_price"
                    ]
                },
                "countrycode": {
                    "type": "string"
                },
                "review_nr": {
                    "type": "number"
                },
                "hotel_name": {
                    "type": "string"
                },
                "has_free_parking": {
                    "type": "number"
                },
                "currencycode": {
                    "type": "string"
                },
                "id": {
                    "type": "string"
                }
                },
                "required": [
                "hotel_id",
                "preferred_plus",
                "class_is_estimated",
                "block_ids",
                "accommodation_type",
                "longitude",
                "latitude",
                "checkout",
                "min_total_price",
                "is_smart_deal",
                "city_in_trans",
                "is_tpi_exclusive_property",
                "timezone",
                "unit_configuration_label",
                "urgency_message",
                "review_score",
                "class",
                "badges",
                "last_reservation_data",
                "extended",
                "checkin",
                "soldout",
                "hotel_has_vb_boost",
                "type",
                "is_genius_deal",
                "has_swimming_pool",
                "is_no_prepayment_block",
                "bwallet",
                "default_wishlist_name",
                "ufi",
                "is_free_cancellable",
                "preferred",
                "main_photo_id",
                "default_language",
                "review_score_word",
                "booking_home",
                "genius_discount_percentage",
                "hotel_name_trans",
                "city",
                "hotel_include_breakfast",
                "composite_price_breakdown",
                "countrycode",
                "review_nr",
                "hotel_name",
                "has_free_parking",
                "currencycode",
                "id"
                ]
            }
            },
            "room_distribution": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                "adults": {
                    "type": "string"
                }
                },
                "required": [
                "adults"
                ]
            }
            },
            "b_max_los_data": {
            "type": "object",
            "properties": {
                "has_extended_los": {
                "type": "number"
                },
                "extended_los": {
                "type": "number"
                },
                "is_fullon": {
                "type": "number"
                },
                "experiment": {
                "type": "string"
                },
                "max_allowed_los": {
                "type": "number"
                },
                "default_los": {
                "type": "number"
                }
            },
            "required": [
                "has_extended_los",
                "extended_los",
                "is_fullon",
                "experiment",
                "max_allowed_los",
                "default_los"
            ]
            },
            "unfiltered_count": {
            "type": "number"
            },
            "unfiltered_primary_count": {
            "type": "number"
            }
        },
        "required": [
            "count",
            "primary_count",
            "extended_count",
            "page_loading_threshold",
            "filters",
            "result",
            "room_distribution",
            "b_max_los_data",
            "unfiltered_count",
            "unfiltered_primary_count"
        ]
        }
    },
    "required": [
        "status",
        "message",
        "data"
    ]
    }    
    """
    def __init__(self, api_response_fpath: str) -> None:
        super().__init__(api_response_fpath)

    def init_task_list(self) -> list[Type[base.Task]]:
        task_list = [
            booking_search_hotel_by_coordinates.GetHotelNumReviews,
            booking_search_hotel_by_coordinates.GetHotelRating,
            booking_search_hotel_by_coordinates.FilterReviewRating,
            booking_search_hotel_by_coordinates.ListHotelParking,
            booking_search_hotel_by_coordinates.AvgHotelPrice,
            booking_search_hotel_by_coordinates.CountExtendedStay,
        ]
        return task_list

class BookingSearchCarRentalsTaskList(TaskList):

    response_json_schema: str = """
    {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Response schema for the search car rentals endpoint.",
    "type": "object",
    "properties": {
        "status": {
        "type": "boolean"
        },
        "message": {
        "type": "string"
        },
        "data": {
        "type": "object",
        "properties": {
            "filter": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                "categories": {
                    "type": "array",
                    "items": {
                    "type": "object",
                    "properties": {
                        "count": {
                        "type": "number"
                        },
                        "nameWithCount": {
                        "type": "string"
                        },
                        "name": {
                        "type": "string"
                        },
                        "id": {
                        "type": "string"
                        }
                    },
                    "required": [
                        "count",
                        "nameWithCount",
                        "name",
                        "id"
                    ]
                    }
                },
                "id": {
                    "type": "string"
                },
                "type": {
                    "type": "string"
                },
                "title": {
                    "type": "string"
                },
                "layout": {
                    "type": "object",
                    "properties": {
                    "is_collapsed": {
                        "type": "string"
                    },
                    "is_collapsable": {
                        "type": "string"
                    },
                    "layout_type": {
                        "type": "string"
                    },
                    "collapsed_count": {
                        "type": "number"
                    }
                    },
                    "required": [
                    "is_collapsed",
                    "is_collapsable",
                    "layout_type",
                    "collapsed_count"
                    ]
                }
                },
                "required": [
                "categories",
                "id",
                "type",
                "title",
                "layout"
                ]
            }
            },
            "is_genius_location": {
            "type": "boolean"
            },
            "content": {
            "type": "object",
            "properties": {
                "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                    "positionInList": {
                        "type": "number"
                    },
                    "content": {
                        "type": "object",
                        "properties": {
                        "contentType": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "contentType"
                        ]
                    },
                    "type": {
                        "type": "string"
                    }
                    },
                    "required": [
                    "positionInList",
                    "content",
                    "type"
                    ]
                }
                },
                "filters": {
                "type": "object",
                "properties": {
                    "countLabel": {
                    "type": "string"
                    }
                },
                "required": [
                    "countLabel"
                ]
                }
            },
            "required": [
                "items",
                "filters"
            ]
            },
            "search_results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                "vehicle_id": {
                    "type": "string"
                },
                "fee_info": {
                    "type": "object",
                    "properties": {
                    "fee": {
                        "type": "number"
                    },
                    "tax": {
                        "type": "number"
                    }
                    },
                    "required": [
                    "fee",
                    "tax"
                    ]
                },
                "rating_info": {
                    "type": "object",
                    "properties": {
                    "no_of_ratings": {
                        "type": "number"
                    },
                    "dropoff_time": {
                        "type": "number"
                    },
                    "location": {
                        "type": "number"
                    },
                    "pickup_time": {
                        "type": "number"
                    },
                    "value_for_money": {
                        "type": "number"
                    },
                    "cleanliness": {
                        "type": "number"
                    },
                    "efficiency": {
                        "type": "number"
                    },
                    "average_text": {
                        "type": "string"
                    },
                    "condition": {
                        "type": "number"
                    },
                    "average": {
                        "type": "number"
                    }
                    },
                    "required": [
                    "no_of_ratings",
                    "dropoff_time",
                    "location",
                    "pickup_time",
                    "value_for_money",
                    "cleanliness",
                    "efficiency",
                    "condition",
                    "average"
                    ]
                },
                "vehicle_info": {
                    "type": "object",
                    "properties": {
                    "airbags": {
                        "type": "number"
                    },
                    "seats": {
                        "type": "string"
                    },
                    "aircon": {
                        "type": "number"
                    },
                    "cma_compliant": {
                        "type": "number"
                    },
                    "fuel_type": {
                        "type": "string"
                    },
                    "free_cancellation": {
                        "type": "number"
                    },
                    "special_offer_text": {
                        "type": "string"
                    },
                    "group": {
                        "type": "string"
                    },
                    "suitcases": {
                        "type": "object",
                        "properties": {
                        "big": {
                            "type": "string"
                        },
                        "small": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "big",
                        "small"
                        ]
                    },
                    "mileage": {
                        "type": "string"
                    },
                    "label": {
                        "type": "string"
                    },
                    "v_id": {
                        "type": "string"
                    },
                    "doors": {
                        "type": "string"
                    },
                    "transmission": {
                        "type": "string"
                    },
                    "v_name": {
                        "type": "string"
                    },
                    "fuel_policy": {
                        "type": "string"
                    },
                    "unlimited_mileage": {
                        "type": "number"
                    }
                    },
                    "required": [
                    "airbags",
                    "seats",
                    "aircon",
                    "cma_compliant",
                    "fuel_type",
                    "free_cancellation",
                    "group",
                    "suitcases",
                    "mileage",
                    "label",
                    "v_id",
                    "doors",
                    "transmission",
                    "v_name",
                    "fuel_policy",
                    "unlimited_mileage"
                    ]
                },
                "content": {
                    "type": "object",
                    "properties": {
                    "badges": {
                        "type": "array",
                        "items": {
                        "type": "object",
                        "properties": {
                            "type": {
                            "type": "string"
                            },
                            "variation": {
                            "type": "string"
                            },
                            "text": {
                            "type": "string"
                            }
                        },
                        "required": [
                            "type",
                            "variation",
                            "text"
                        ]
                        }
                    },
                    "supplier": {
                        "type": "object",
                        "properties": {
                        "rating": {
                            "type": "object",
                            "properties": {
                            "subtitle": {
                                "type": "string"
                            },
                            "localisedRating": {
                                "type": "object",
                                "properties": {
                                "displayValue": {
                                    "type": "string"
                                },
                                "rawValue": {
                                    "type": "number"
                                }
                                },
                                "required": [
                                "displayValue",
                                "rawValue"
                                ]
                            },
                            "title": {
                                "type": "string"
                            },
                            "average": {
                                "type": "string"
                            }
                            },
                            "required": [
                            "subtitle",
                            "localisedRating",
                            "title",
                            "average"
                            ]
                        },
                        "name": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "name"
                        ]
                    }
                    },
                    "required": [
                    "badges",
                    "supplier"
                    ]
                },
                "route_info": {
                    "type": "object",
                    "properties": {
                    "pickup": {
                        "type": "object",
                        "properties": {
                        "longitude": {
                            "type": "string"
                        },
                        "location_type": {
                            "type": "string"
                        },
                        "name": {
                            "type": "string"
                        },
                        "latitude": {
                            "type": "string"
                        },
                        "location_hash": {
                            "type": "string"
                        },
                        "location_id": {
                            "type": "string"
                        },
                        "address": {
                            "type": "string"
                        },
                        "country_code": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "longitude",
                        "location_type",
                        "name",
                        "latitude",
                        "location_hash",
                        "location_id",
                        "address",
                        "country_code"
                        ]
                    },
                    "dropoff": {
                        "type": "object",
                        "properties": {
                        "address": {
                            "type": "string"
                        },
                        "country_code": {
                            "type": "string"
                        },
                        "location_hash": {
                            "type": "string"
                        },
                        "location_id": {
                            "type": "string"
                        },
                        "longitude": {
                            "type": "string"
                        },
                        "location_type": {
                            "type": "string"
                        },
                        "name": {
                            "type": "string"
                        },
                        "latitude": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "address",
                        "country_code",
                        "location_hash",
                        "location_id",
                        "longitude",
                        "location_type",
                        "name",
                        "latitude"
                        ]
                    }
                    },
                    "required": [
                    "pickup",
                    "dropoff"
                    ]
                },
                "accessibility": {
                    "type": "object",
                    "properties": {
                    "transmission": {
                        "type": "string"
                    },
                    "pick_up_location": {
                        "type": "string"
                    },
                    "fuel_policy": {
                        "type": "string"
                    },
                    "supplier_rating": {
                        "type": "string"
                    }
                    },
                    "required": [
                    "transmission",
                    "pick_up_location",
                    "fuel_policy",
                    "supplier_rating"
                    ]
                },
                "supplier_info": {
                    "type": "object",
                    "properties": {
                    "pickup_instructions": {
                        "type": "string"
                    },
                    "address": {
                        "type": "string"
                    },
                    "logo_url": {
                        "type": "string"
                    },
                    "latitude": {
                        "type": "string"
                    },
                    "name": {
                        "type": "string"
                    },
                    "location_type": {
                        "type": "string"
                    },
                    "longitude": {
                        "type": "string"
                    },
                    "may_require_credit_card_guarantee": {
                        "type": "boolean"
                    },
                    "dropoff_instructions": {
                        "type": "string"
                    }
                    },
                    "required": [
                    "pickup_instructions",
                    "address",
                    "logo_url",
                    "latitude",
                    "name",
                    "location_type",
                    "longitude",
                    "may_require_credit_card_guarantee",
                    "dropoff_instructions"
                    ]
                },
                "pricing_info": {
                    "type": "object",
                    "properties": {
                    "fee_breakdown": {
                        "type": "object",
                        "properties": {
                        "known_fees": {
                            "type": "array",
                            "items": {
                            "type": "object",
                            "properties": {
                                "max_amount": {
                                "type": "number"
                                },
                                "is_tax_included": {
                                "type": "number"
                                },
                                "currency": {
                                "type": "string"
                                },
                                "min_amount": {
                                "type": "number"
                                },
                                "type": {
                                "type": "string"
                                },
                                "amount": {
                                "type": "number"
                                },
                                "is_always_payable": {
                                "type": "number"
                                },
                                "distance_allowed": {
                                "type": "object",
                                "properties": {
                                    "is_unlimited": {
                                    "type": "number"
                                    },
                                    "is_km": {
                                    "type": "number"
                                    }
                                },
                                "required": [
                                    "is_unlimited",
                                    "is_km"
                                ]
                                }
                            },
                            "required": [
                                "type",
                                "is_always_payable"
                            ]
                            }
                        },
                        "fuel_policy": {
                            "type": "object",
                            "properties": {
                            "type": {
                                "type": "string"
                            },
                            "amount": {
                                "type": "number"
                            }
                            },
                            "required": [
                            "type",
                            "amount"
                            ]
                        }
                        },
                        "required": [
                        "known_fees",
                        "fuel_policy"
                        ]
                    },
                    "price": {
                        "type": "number"
                    },
                    "drive_away_price": {
                        "type": "number"
                    },
                    "base_currency": {
                        "type": "string"
                    },
                    "pay_when": {
                        "type": "string"
                    },
                    "deposit": {
                        "type": "number"
                    },
                    "currency": {
                        "type": "string"
                    },
                    "base_price": {
                        "type": "number"
                    },
                    "discount": {
                        "type": "number"
                    },
                    "drive_away_price_is_approx": {
                        "type": "boolean"
                    },
                    "base_deposit": {
                        "type": "number"
                    },
                    "quote_allowed": {
                        "type": "number"
                    }
                    },
                    "required": [
                    "fee_breakdown",
                    "price",
                    "drive_away_price",
                    "base_currency",
                    "pay_when",
                    "deposit",
                    "currency",
                    "base_price",
                    "discount",
                    "drive_away_price_is_approx",
                    "base_deposit",
                    "quote_allowed"
                    ]
                },
                "freebies": {
                    "type": "array",
                    "items": {
                    "type": "string"
                    }
                }
                },
                "required": [
                "vehicle_id",
                "fee_info",
                "rating_info",
                "vehicle_info",
                "content",
                "route_info",
                "accessibility",
                "supplier_info",
                "pricing_info",
                "freebies"
                ]
            }
            },
            "search_context": {
            "type": "object",
            "properties": {
                "searchKey": {
                "type": "string"
                },
                "searchId": {
                "type": "string"
                },
                "recommendationsSearchUniqueId": {
                "type": "string"
                }
            },
            "required": [
                "searchKey",
                "searchId",
                "recommendationsSearchUniqueId"
            ]
            },
            "count": {
            "type": "number"
            },
            "meta": {
            "type": "object",
            "properties": {
                "response_code": {
                "type": "number"
                }
            },
            "required": [
                "response_code"
            ]
            },
            "title": {
            "type": "string"
            },
            "type": {
            "type": "string"
            },
            "sort": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                "title_tag": {
                    "type": "string"
                },
                "identifier": {
                    "type": "string"
                },
                "name": {
                    "type": "string"
                }
                },
                "required": [
                "title_tag",
                "identifier",
                "name"
                ]
            }
            },
            "search_key": {
            "type": "string"
            },
            "provider": {
            "type": "string"
            }
        },
        "required": [
            "filter",
            "is_genius_location",
            "content",
            "search_results",
            "search_context",
            "count",
            "meta",
            "title",
            "type",
            "sort",
            "search_key",
            "provider"
        ]
        }
    },
    "required": [
        "status",
        "message",
        "data"
    ]
    }
    """
    def __init__(self, api_response_fpath: str) -> None:
        super().__init__(api_response_fpath)

    def init_task_list(self) -> list[Type[base.Task]]:
        task_list = [
            booking_search_car_rentals.GetCleanlinessRating,
            booking_search_car_rentals.GetFuelPolicy,
            booking_search_car_rentals.ListCarInCurrency,
            booking_search_car_rentals.ListCarFreeCancellation,
            booking_search_car_rentals.CountCarsByTransmission,
            booking_search_car_rentals.CheapestCar,
        ]
        return task_list


class BookingGetSeatMapTaskList(TaskList):
    response_json_schema: str = """
    {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Response schema for the get seat map endpoint.",
    "type": "object",
    "properties": {
        "status": {
        "type": "boolean"
        },
        "message": {
        "type": "string"
        },
        "data": {
        "type": "object",
        "properties": {
            "checkedInBaggage": {
            "type": "object",
            "properties": {
                "airProductReference": {
                "type": "string"
                },
                "options": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                    "luggageAllowance": {
                        "type": "object",
                        "properties": {
                        "luggageType": {
                            "type": "string"
                        },
                        "ruleType": {
                            "type": "string"
                        },
                        "maxPiece": {
                            "type": "number"
                        },
                        "maxWeightPerPiece": {
                            "type": "number"
                        },
                        "massUnit": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "luggageType",
                        "ruleType",
                        "maxPiece",
                        "maxWeightPerPiece",
                        "massUnit"
                        ]
                    },
                    "priceBreakdown": {
                        "type": "object",
                        "properties": {
                        "total": {
                            "type": "object",
                            "properties": {
                            "currencyCode": {
                                "type": "string"
                            },
                            "units": {
                                "type": "number"
                            },
                            "nanos": {
                                "type": "number"
                            }
                            },
                            "required": [
                            "currencyCode",
                            "units",
                            "nanos"
                            ]
                        },
                        "baseFare": {
                            "type": "object",
                            "properties": {
                            "currencyCode": {
                                "type": "string"
                            },
                            "units": {
                                "type": "number"
                            },
                            "nanos": {
                                "type": "number"
                            }
                            },
                            "required": [
                            "currencyCode",
                            "units",
                            "nanos"
                            ]
                        },
                        "fee": {
                            "type": "object",
                            "properties": {
                            "currencyCode": {
                                "type": "string"
                            },
                            "units": {
                                "type": "number"
                            },
                            "nanos": {
                                "type": "number"
                            }
                            },
                            "required": [
                            "currencyCode",
                            "units",
                            "nanos"
                            ]
                        },
                        "tax": {
                            "type": "object",
                            "properties": {
                            "currencyCode": {
                                "type": "string"
                            },
                            "units": {
                                "type": "number"
                            },
                            "nanos": {
                                "type": "number"
                            }
                            },
                            "required": [
                            "currencyCode",
                            "units",
                            "nanos"
                            ]
                        },
                        "discount": {
                            "type": "object",
                            "properties": {
                            "currencyCode": {
                                "type": "string"
                            },
                            "units": {
                                "type": "number"
                            },
                            "nanos": {
                                "type": "number"
                            }
                            },
                            "required": [
                            "currencyCode",
                            "units",
                            "nanos"
                            ]
                        },
                        "totalWithoutDiscount": {
                            "type": "object",
                            "properties": {
                            "currencyCode": {
                                "type": "string"
                            },
                            "units": {
                                "type": "number"
                            },
                            "nanos": {
                                "type": "number"
                            }
                            },
                            "required": [
                            "currencyCode",
                            "units",
                            "nanos"
                            ]
                        }
                        },
                        "required": [
                        "total",
                        "baseFare",
                        "fee",
                        "tax",
                        "discount",
                        "totalWithoutDiscount"
                        ]
                    },
                    "travellers": {
                        "type": "array",
                        "items": {
                        "type": "string"
                        }
                    },
                    "preSelected": {
                        "type": "boolean"
                    }
                    },
                    "required": [
                    "luggageAllowance",
                    "priceBreakdown",
                    "travellers",
                    "preSelected"
                    ]
                }
                }
            },
            "required": [
                "airProductReference",
                "options"
            ]
            },
            "flexibleTicket": {
            "type": "object",
            "properties": {
                "airProductReference": {
                "type": "string"
                },
                "travellers": {
                "type": "array",
                "items": {
                    "type": "string"
                }
                },
                "priceBreakdown": {
                "type": "object",
                "properties": {
                    "total": {
                    "type": "object",
                    "properties": {
                        "currencyCode": {
                        "type": "string"
                        },
                        "units": {
                        "type": "number"
                        },
                        "nanos": {
                        "type": "number"
                        }
                    },
                    "required": [
                        "currencyCode",
                        "units",
                        "nanos"
                    ]
                    },
                    "baseFare": {
                    "type": "object",
                    "properties": {
                        "currencyCode": {
                        "type": "string"
                        },
                        "units": {
                        "type": "number"
                        },
                        "nanos": {
                        "type": "number"
                        }
                    },
                    "required": [
                        "currencyCode",
                        "units",
                        "nanos"
                    ]
                    },
                    "fee": {
                    "type": "object",
                    "properties": {
                        "currencyCode": {
                        "type": "string"
                        },
                        "units": {
                        "type": "number"
                        },
                        "nanos": {
                        "type": "number"
                        }
                    },
                    "required": [
                        "currencyCode",
                        "units",
                        "nanos"
                    ]
                    },
                    "tax": {
                    "type": "object",
                    "properties": {
                        "currencyCode": {
                        "type": "string"
                        },
                        "units": {
                        "type": "number"
                        },
                        "nanos": {
                        "type": "number"
                        }
                    },
                    "required": [
                        "currencyCode",
                        "units",
                        "nanos"
                    ]
                    },
                    "discount": {
                    "type": "object",
                    "properties": {
                        "currencyCode": {
                        "type": "string"
                        },
                        "units": {
                        "type": "number"
                        },
                        "nanos": {
                        "type": "number"
                        }
                    },
                    "required": [
                        "currencyCode",
                        "units",
                        "nanos"
                    ]
                    },
                    "totalWithoutDiscount": {
                    "type": "object",
                    "properties": {
                        "currencyCode": {
                        "type": "string"
                        },
                        "units": {
                        "type": "number"
                        },
                        "nanos": {
                        "type": "number"
                        }
                    },
                    "required": [
                        "currencyCode",
                        "units",
                        "nanos"
                    ]
                    }
                },
                "required": [
                    "total",
                    "baseFare",
                    "fee",
                    "tax",
                    "discount",
                    "totalWithoutDiscount"
                ]
                },
                "preSelected": {
                "type": "boolean"
                },
                "recommendation": {
                "type": "object",
                "properties": {
                    "recommended": {
                    "type": "boolean"
                    },
                    "confidence": {
                    "type": "string"
                    }
                },
                "required": [
                    "recommended",
                    "confidence"
                ]
                },
                "supplierInfo": {
                "type": "object",
                "properties": {
                    "name": {
                    "type": "string"
                    }
                },
                "required": [
                    "name"
                ]
                }
            },
            "required": [
                "airProductReference",
                "travellers",
                "priceBreakdown",
                "preSelected",
                "recommendation",
                "supplierInfo"
            ]
            },
            "mealPreference": {
            "type": "object",
            "properties": {
                "airProductReference": {
                "type": "string"
                },
                "travellers": {
                "type": "array",
                "items": {
                    "type": "string"
                }
                },
                "choices": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                    "mealType": {
                        "type": "string"
                    },
                    "priceBreakdown": {
                        "type": "object",
                        "properties": {
                        "total": {
                            "type": "object",
                            "properties": {
                            "currencyCode": {
                                "type": "string"
                            },
                            "units": {
                                "type": "number"
                            },
                            "nanos": {
                                "type": "number"
                            }
                            },
                            "required": [
                            "currencyCode",
                            "units",
                            "nanos"
                            ]
                        },
                        "baseFare": {
                            "type": "object",
                            "properties": {
                            "currencyCode": {
                                "type": "string"
                            },
                            "units": {
                                "type": "number"
                            },
                            "nanos": {
                                "type": "number"
                            }
                            },
                            "required": [
                            "currencyCode",
                            "units",
                            "nanos"
                            ]
                        },
                        "fee": {
                            "type": "object",
                            "properties": {
                            "currencyCode": {
                                "type": "string"
                            },
                            "units": {
                                "type": "number"
                            },
                            "nanos": {
                                "type": "number"
                            }
                            },
                            "required": [
                            "currencyCode",
                            "units",
                            "nanos"
                            ]
                        },
                        "tax": {
                            "type": "object",
                            "properties": {
                            "currencyCode": {
                                "type": "string"
                            },
                            "units": {
                                "type": "number"
                            },
                            "nanos": {
                                "type": "number"
                            }
                            },
                            "required": [
                            "currencyCode",
                            "units",
                            "nanos"
                            ]
                        },
                        "discount": {
                            "type": "object",
                            "properties": {
                            "currencyCode": {
                                "type": "string"
                            },
                            "units": {
                                "type": "number"
                            },
                            "nanos": {
                                "type": "number"
                            }
                            },
                            "required": [
                            "currencyCode",
                            "units",
                            "nanos"
                            ]
                        },
                        "totalWithoutDiscount": {
                            "type": "object",
                            "properties": {
                            "currencyCode": {
                                "type": "string"
                            },
                            "units": {
                                "type": "number"
                            },
                            "nanos": {
                                "type": "number"
                            }
                            },
                            "required": [
                            "currencyCode",
                            "units",
                            "nanos"
                            ]
                        }
                        },
                        "required": [
                        "total",
                        "baseFare",
                        "fee",
                        "tax",
                        "discount",
                        "totalWithoutDiscount"
                        ]
                    }
                    },
                    "required": [
                    "mealType",
                    "priceBreakdown"
                    ]
                }
                }
            },
            "required": [
                "airProductReference",
                "travellers",
                "choices"
            ]
            },
            "mobileTravelPlan": {
            "type": "object",
            "properties": {
                "priceBreakdown": {
                "type": "object",
                "properties": {
                    "total": {
                    "type": "object",
                    "properties": {
                        "currencyCode": {
                        "type": "string"
                        },
                        "units": {
                        "type": "number"
                        },
                        "nanos": {
                        "type": "number"
                        }
                    },
                    "required": [
                        "currencyCode",
                        "units",
                        "nanos"
                    ]
                    },
                    "baseFare": {
                    "type": "object",
                    "properties": {
                        "currencyCode": {
                        "type": "string"
                        },
                        "units": {
                        "type": "number"
                        },
                        "nanos": {
                        "type": "number"
                        }
                    },
                    "required": [
                        "currencyCode",
                        "units",
                        "nanos"
                    ]
                    },
                    "fee": {
                    "type": "object",
                    "properties": {
                        "currencyCode": {
                        "type": "string"
                        },
                        "units": {
                        "type": "number"
                        },
                        "nanos": {
                        "type": "number"
                        }
                    },
                    "required": [
                        "currencyCode",
                        "units",
                        "nanos"
                    ]
                    },
                    "tax": {
                    "type": "object",
                    "properties": {
                        "currencyCode": {
                        "type": "string"
                        },
                        "units": {
                        "type": "number"
                        },
                        "nanos": {
                        "type": "number"
                        }
                    },
                    "required": [
                        "currencyCode",
                        "units",
                        "nanos"
                    ]
                    },
                    "discount": {
                    "type": "object",
                    "properties": {
                        "currencyCode": {
                        "type": "string"
                        },
                        "units": {
                        "type": "number"
                        },
                        "nanos": {
                        "type": "number"
                        }
                    },
                    "required": [
                        "currencyCode",
                        "units",
                        "nanos"
                    ]
                    },
                    "totalWithoutDiscount": {
                    "type": "object",
                    "properties": {
                        "currencyCode": {
                        "type": "string"
                        },
                        "units": {
                        "type": "number"
                        },
                        "nanos": {
                        "type": "number"
                        }
                    },
                    "required": [
                        "currencyCode",
                        "units",
                        "nanos"
                    ]
                    }
                },
                "required": [
                    "total",
                    "baseFare",
                    "fee",
                    "tax",
                    "discount",
                    "totalWithoutDiscount"
                ]
                }
            },
            "required": [
                "priceBreakdown"
            ]
            },
            "seatMap": {
            "type": "object",
            "properties": {
                "airProductReference": {
                "type": "string"
                },
                "seatMapOption": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                    "cabins": {
                        "type": "array",
                        "items": {
                        "type": "object",
                        "properties": {
                            "class": {
                            "type": "string"
                            },
                            "deck": {
                            "type": "string"
                            },
                            "columns": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                "id": {
                                    "type": "string"
                                },
                                "description": {
                                    "type": "array",
                                    "items": {
                                    "type": "string"
                                    }
                                }
                                },
                                "required": [
                                "id",
                                "description"
                                ]
                            }
                            },
                            "rows": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                "id": {
                                    "type": "number"
                                },
                                "seats": {
                                    "type": "array",
                                    "items": {
                                    "type": "object",
                                    "properties": {
                                        "colId": {
                                        "type": "string"
                                        },
                                        "description": {
                                        "type": "string"
                                        },
                                        "priceBreakdown": {
                                        "type": "object",
                                        "properties": {
                                            "total": {
                                            "type": "object",
                                            "properties": {
                                                "currencyCode": {
                                                "type": "string"
                                                },
                                                "units": {
                                                "type": "number"
                                                },
                                                "nanos": {
                                                "type": "number"
                                                }
                                            },
                                            "required": [
                                                "currencyCode",
                                                "units",
                                                "nanos"
                                            ]
                                            },
                                            "baseFare": {
                                            "type": "object",
                                            "properties": {
                                                "currencyCode": {
                                                "type": "string"
                                                },
                                                "units": {
                                                "type": "number"
                                                },
                                                "nanos": {
                                                "type": "number"
                                                }
                                            },
                                            "required": [
                                                "currencyCode",
                                                "units",
                                                "nanos"
                                            ]
                                            },
                                            "fee": {
                                            "type": "object",
                                            "properties": {
                                                "currencyCode": {
                                                "type": "string"
                                                },
                                                "units": {
                                                "type": "number"
                                                },
                                                "nanos": {
                                                "type": "number"
                                                }
                                            },
                                            "required": [
                                                "currencyCode",
                                                "units",
                                                "nanos"
                                            ]
                                            },
                                            "tax": {
                                            "type": "object",
                                            "properties": {
                                                "currencyCode": {
                                                "type": "string"
                                                },
                                                "units": {
                                                "type": "number"
                                                },
                                                "nanos": {
                                                "type": "number"
                                                }
                                            },
                                            "required": [
                                                "currencyCode",
                                                "units",
                                                "nanos"
                                            ]
                                            },
                                            "discount": {
                                            "type": "object",
                                            "properties": {
                                                "currencyCode": {
                                                "type": "string"
                                                },
                                                "units": {
                                                "type": "number"
                                                },
                                                "nanos": {
                                                "type": "number"
                                                }
                                            },
                                            "required": [
                                                "currencyCode",
                                                "units",
                                                "nanos"
                                            ]
                                            },
                                            "totalWithoutDiscount": {
                                            "type": "object",
                                            "properties": {
                                                "currencyCode": {
                                                "type": "string"
                                                },
                                                "units": {
                                                "type": "number"
                                                },
                                                "nanos": {
                                                "type": "number"
                                                }
                                            },
                                            "required": [
                                                "currencyCode",
                                                "units",
                                                "nanos"
                                            ]
                                            }
                                        },
                                        "required": [
                                            "total",
                                            "baseFare",
                                            "fee",
                                            "tax",
                                            "discount",
                                            "totalWithoutDiscount"
                                        ]
                                        }
                                    },
                                    "required": [
                                        "colId",
                                        "description"
                                    ]
                                    }
                                },
                                "description": {
                                    "type": "array",
                                    "items": {
                                    "type": "string"
                                    }
                                }
                                },
                                "required": [
                                "id",
                                "seats"
                                ]
                            }
                            }
                        },
                        "required": [
                            "class",
                            "deck",
                            "columns",
                            "rows"
                        ]
                        }
                    },
                    "segmentIndex": {
                        "type": "number"
                    },
                    "legIndex": {
                        "type": "number"
                    },
                    "travellers": {
                        "type": "array",
                        "items": {
                        "type": "string"
                        }
                    }
                    },
                    "required": [
                    "cabins",
                    "segmentIndex",
                    "legIndex",
                    "travellers"
                    ]
                }
                }
            },
            "required": [
                "airProductReference",
                "seatMapOption"
            ]
            },
            "travelInsurance": {
            "type": "object",
            "properties": {
                "options": {
                "type": "object",
                "properties": {
                    "type": {
                    "type": "string"
                    },
                    "travellers": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                    },
                    "priceBreakdown": {
                    "type": "object",
                    "properties": {
                        "total": {
                        "type": "object",
                        "properties": {
                            "currencyCode": {
                            "type": "string"
                            },
                            "units": {
                            "type": "number"
                            },
                            "nanos": {
                            "type": "number"
                            }
                        },
                        "required": [
                            "currencyCode",
                            "units",
                            "nanos"
                        ]
                        },
                        "baseFare": {
                        "type": "object",
                        "properties": {
                            "currencyCode": {
                            "type": "string"
                            },
                            "units": {
                            "type": "number"
                            },
                            "nanos": {
                            "type": "number"
                            }
                        },
                        "required": [
                            "currencyCode",
                            "units",
                            "nanos"
                        ]
                        },
                        "fee": {
                        "type": "object",
                        "properties": {
                            "currencyCode": {
                            "type": "string"
                            },
                            "units": {
                            "type": "number"
                            },
                            "nanos": {
                            "type": "number"
                            }
                        },
                        "required": [
                            "currencyCode",
                            "units",
                            "nanos"
                        ]
                        },
                        "tax": {
                        "type": "object",
                        "properties": {
                            "currencyCode": {
                            "type": "string"
                            },
                            "units": {
                            "type": "number"
                            },
                            "nanos": {
                            "type": "number"
                            }
                        },
                        "required": [
                            "currencyCode",
                            "units",
                            "nanos"
                        ]
                        },
                        "discount": {
                        "type": "object",
                        "properties": {
                            "currencyCode": {
                            "type": "string"
                            },
                            "units": {
                            "type": "number"
                            },
                            "nanos": {
                            "type": "number"
                            }
                        },
                        "required": [
                            "currencyCode",
                            "units",
                            "nanos"
                        ]
                        },
                        "totalWithoutDiscount": {
                        "type": "object",
                        "properties": {
                            "currencyCode": {
                            "type": "string"
                            },
                            "units": {
                            "type": "number"
                            },
                            "nanos": {
                            "type": "number"
                            }
                        },
                        "required": [
                            "currencyCode",
                            "units",
                            "nanos"
                        ]
                        }
                    },
                    "required": [
                        "total",
                        "baseFare",
                        "fee",
                        "tax",
                        "discount",
                        "totalWithoutDiscount"
                    ]
                    },
                    "disclaimer": {
                    "type": "string"
                    }
                },
                "required": [
                    "type",
                    "travellers",
                    "priceBreakdown",
                    "disclaimer"
                ]
                },
                "content": {
                "type": "object",
                "properties": {
                    "header": {
                    "type": "string"
                    },
                    "subheader": {
                    "type": "string"
                    },
                    "optInTitle": {
                    "type": "string"
                    },
                    "optOutTitle": {
                    "type": "string"
                    },
                    "exclusions": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                    },
                    "coveredStatusLabel": {
                    "type": "string"
                    },
                    "notCoveredStatusLabel": {
                    "type": "string"
                    },
                    "benefitsTitle": {
                    "type": "string"
                    },
                    "closeA11y": {
                    "type": "string"
                    },
                    "benefits": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                    },
                    "finePrint": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                    }
                },
                "required": [
                    "header",
                    "subheader",
                    "optInTitle",
                    "optOutTitle",
                    "exclusions",
                    "coveredStatusLabel",
                    "notCoveredStatusLabel",
                    "benefitsTitle",
                    "closeA11y",
                    "benefits",
                    "finePrint"
                ]
                },
                "forceForAllTravellers": {
                "type": "boolean"
                },
                "isPerTraveller": {
                "type": "boolean"
                },
                "recommendation": {
                "type": "object",
                "properties": {
                    "recommended": {
                    "type": "boolean"
                    },
                    "confidence": {
                    "type": "string"
                    }
                },
                "required": [
                    "recommended",
                    "confidence"
                ]
                }
            },
            "required": [
                "options",
                "content",
                "forceForAllTravellers",
                "isPerTraveller",
                "recommendation"
            ]
            }
        },
        "required": [
            "checkedInBaggage",
            "flexibleTicket",
            "mealPreference",
            "mobileTravelPlan",
            "seatMap",
            "travelInsurance"
        ]
        }
    },
    "required": [
        "status",
        "message",
        "data"
    ]
    }    

    """

    def __init__(self, api_response_fpath: str) -> None:
        super().__init__(api_response_fpath)

    def init_task_list(self) -> list[Type[base.Task]]:
        task_list = [
            booking_get_seat_map.GetInsurancePrice,
            booking_get_seat_map.GetLuggageAllowance,
            booking_get_seat_map.ListSeatOptions,
            booking_get_seat_map.ListSeatOptionsBySeatType,
            booking_get_seat_map.CountSeatOptions,
            booking_get_seat_map.PercentSeatType,
        ]
        return task_list

class SECFilingsTaskList(TaskList):
    response_json_schema: str = """
    {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "Response schema for the SEC filings endpoint.",
        "type": "object",
        "properties": {
            "meta": {
            "type": "object",
            "properties": {
                "copyright": {
                "type": "string"
                },
                "terms": {
                "type": "array",
                "items": {
                    "type": "string"
                }
                }
            },
            "required": [
                "copyright",
                "terms"
            ]
            },
            "data": {
            "type": "object",
            "properties": {
                "attributes": {
                "type": "object",
                "properties": {
                    "status": {
                    "type": "number"
                    },
                    "company": {
                    "type": "object",
                    "properties": {
                        "name": {
                        "type": "string"
                        },
                        "cik": {
                        "type": "string"
                        },
                        "ticker": {
                        "type": "string"
                        }
                    },
                    "required": [
                        "name",
                        "cik",
                        "ticker"
                    ]
                    },
                    "count": {
                    "type": "number"
                    },
                    "result": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                        "name": {
                            "type": "string"
                        },
                        "accessionNumber": {
                            "type": "string"
                        },
                        "filingDate": {
                            "type": "string"
                        },
                        "formType": {
                            "type": "string"
                        },
                        "url": {
                            "type": "string"
                        },
                        "period": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "name",
                        "accessionNumber",
                        "filingDate",
                        "formType",
                        "url"
                        ]
                    }
                    }
                },
                "required": [
                    "status",
                    "company",
                    "count",
                    "result"
                ]
                },
                "type": {
                "type": "string"
                },
                "id": {
                "type": "string"
                }
            },
            "required": [
                "attributes",
                "type",
                "id"
            ]
            },
            "status": {
            "type": "boolean"
            }
        },
        "required": [
            "meta",
            "data",
            "status"
        ]
    }"""

    def __init__(self, api_response_fpath: str) -> None:
        super().__init__(api_response_fpath)

    def init_task_list(self) -> list[Type[base.Task]]:
        task_list = [
            SEC_filings.GetFormType,
            SEC_filings.GetFilingDate,
            SEC_filings.GetFilingName,
            SEC_filings.FilingsInAYear,
            SEC_filings.FilingsOfSpecificFormType,
            SEC_filings.FilingsOfSpecificName,
            SEC_filings.FilingsWithNameAndType,
            SEC_filings.FilingsAccordingToFilingDateAndPeriod,
            SEC_filings.FormTypes,
            SEC_filings.AccessionNumberAsPerFormTypeAndDate,
            SEC_filings.AccessionNumberAsPerSameDate,
            SEC_filings.FilingsName,
            SEC_filings.AccessionNumberAsPerDateName,
        ]
        return task_list

class ProductDetailsShoesTaskList(TaskList):
    response_json_schema: str = """
        {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "title": "API response schema for product shoes.",
        "type": "object",
        "properties": {
            "status": {
            "type": "string"
            },
            "request_id": {
            "type": "string"
            },
            "data": {
            "type": "object",
            "properties": {
                "products": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                    "product_id": {
                        "type": "string"
                    },
                    "product_title": {
                        "type": "string"
                    },
                    "product_description": {
                        "type": "string"
                    },
                    "product_photos": {
                        "type": "array",
                        "items": {
                        "type": "string"
                        }
                    },
                    "product_attributes": {
                        "type": "object",
                        "properties": {
                        "Size": {
                            "type": "string"
                        },
                        "Brand": {
                            "type": "string"
                        },
                        "Width": {
                            "type": "string"
                        },
                        "Material": {
                            "type": "string"
                        },
                        "Color": {
                            "type": "string"
                        },
                        "Style": {
                            "type": "string"
                        },
                        "Outsole Material": {
                            "type": "string"
                        },
                        "Department": {
                            "type": "string"
                        },
                        "Athletic Style": {
                            "type": "string"
                        },
                        "Closure Style": {
                            "type": "string"
                        },
                        "For Athletics": {
                            "type": "string"
                        },
                        "Care Instructions": {
                            "type": "string"
                        },
                        "Support Type": {
                            "type": "string"
                        },
                        "Fashion Sneaker": {
                            "type": "string"
                        },
                        "Type": {
                            "type": "string"
                        },
                        "High-top": {
                            "type": "string"
                        },
                        "Season": {
                            "type": "string"
                        },
                        "Embellishment Style": {
                            "type": "string"
                        },
                        "Breathable": {
                            "type": "string"
                        },
                        "Lining Material": {
                            "type": "string"
                        },
                        "Reflective": {
                            "type": "string"
                        },
                        "For Orthotics": {
                            "type": "string"
                        },
                        "With Composite Toe": {
                            "type": "string"
                        },
                        "Static Dissipative": {
                            "type": "string"
                        },
                        "Slip Resistant": {
                            "type": "string"
                        },
                        "EH Rated": {
                            "type": "string"
                        },
                        "Moisture Wicking": {
                            "type": "string"
                        },
                        "Work": {
                            "type": "string"
                        },
                        "Weight": {
                            "type": "string"
                        },
                        "Toe Shape": {
                            "type": "string"
                        },
                        "Gender": {
                            "type": "string"
                        },
                        "Category": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "Size",
                        "Width"
                        ]
                    },
                    "product_rating": {
                        "type": "number"
                    },
                    "product_page_url": {
                        "type": "string"
                    },
                    "product_offers_page_url": {
                        "type": "string"
                    },
                    "product_specs_page_url": {
                        "type": "string"
                    },
                    "product_reviews_page_url": {
                        "type": "string"
                    },
                    "product_page_url_v2": {
                        "type": "string"
                    },
                    "product_num_reviews": {
                        "type": "number"
                    },
                    "product_num_offers": {
                        "type": "string"
                    },
                    "typical_price_range": {
                        "type": "array",
                        "items": {
                        "type": "string"
                        }
                    },
                    "product_variant_properties": {
                        "type": "object",
                        "properties": {
                        "Size": {
                            "type": "string"
                        },
                        "Color": {
                            "type": "string"
                        },
                        "Width": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "Size"
                        ]
                    },
                    "product_variants": {
                        "type": "object",
                        "properties": {
                        "Size": {
                            "type": "array",
                            "items": {
                            "type": "object",
                            "properties": {
                                "value": {
                                "type": "string"
                                }
                            },
                            "required": [
                                "value"
                            ]
                            }
                        },
                        "Color": {
                            "type": "array",
                            "items": {
                            "type": "object",
                            "properties": {
                                "value": {
                                "type": "string"
                                },
                                "product_id": {
                                "type": "string"
                                },
                                "thumbnail": {
                                "type": "string"
                                }
                            },
                            "required": [
                                "value"
                            ]
                            }
                        },
                        "Width": {
                            "type": "array",
                            "items": {
                            "type": "object",
                            "properties": {
                                "value": {
                                "type": "string"
                                }
                            },
                            "required": [
                                "value"
                            ]
                            }
                        }
                        },
                        "required": [
                        "Size"
                        ]
                    },
                    "offer": {
                        "type": "object",
                        "properties": {
                        "offer_id": {
                            "type": "string"
                        },
                        "offer_page_url": {
                            "type": "string"
                        },
                        "price": {
                            "type": "string"
                        },
                        "shipping": {
                            "type": "string"
                        },
                        "on_sale": {
                            "type": "boolean"
                        },
                        "original_price": {
                            "type": "string"
                        },
                        "product_condition": {
                            "type": "string"
                        },
                        "store_name": {
                            "type": "string"
                        },
                        "store_rating": {
                            "type": "string"
                        },
                        "store_review_count": {
                            "type": "number"
                        },
                        "store_reviews_page_url": {
                            "type": "string"
                        },
                        "store_favicon": {
                            "type": "string"
                        },
                        "coupon_discount_percent": {
                            "type": "string"
                        },
                        "payment_methods": {
                            "type": "string"
                        }
                        },
                        "required": [
                        "offer_id",
                        "offer_page_url",
                        "price",
                        "shipping",
                        "on_sale",
                        "product_condition",
                        "store_name",
                        "store_rating",
                        "store_review_count",
                        "store_reviews_page_url",
                        "store_favicon",
                        "payment_methods"
                        ]
                    }
                    },
                    "required": [
                    "product_id",
                    "product_title",
                    "product_photos",
                    "product_attributes",
                    "product_page_url",
                    "product_offers_page_url",
                    "product_specs_page_url",
                    "product_reviews_page_url",
                    "product_page_url_v2",
                    "product_num_offers",
                    "offer"
                    ]
                }
                },
                "sponsored_products": {
                "type": "array",
                "items": {}
                }
            },
            "required": [
                "products",
                "sponsored_products"
            ]
            }
        },
        "required": [
            "status",
            "request_id",
            "data"
        ]
        }    
    """
    def __init__(self, api_response_fpath: str) -> None:
        super().__init__(api_response_fpath)

    def init_task_list(self) -> list[Type[base.Task]]:
        task_list = [
            product_details_shoes.GetShoeDepartment,
            product_details_shoes.GetProductRating,
            product_details_shoes.GetProductTitle,
            product_details_shoes.ShoeColours,
            product_details_shoes.ShoesInEachDepartment,
            product_details_shoes.ShoeSize,
            product_details_shoes.ShoeMaterialType,
            product_details_shoes.OfferedProductPrice,
            product_details_shoes.ShoesInMultipleColours,
            product_details_shoes.GetShoesColorsAsPerDeptAndRating,
            product_details_shoes.GetProductIdOfTrainerShoes,
            product_details_shoes.ShoesOnSaleAndFreeDelivery,
            product_details_shoes.ProductsIDsHavingDiscount,
        ]

        return task_list
