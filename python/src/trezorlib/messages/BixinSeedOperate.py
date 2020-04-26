# Automatically generated by pb2py
# fmt: off
from .. import protobuf as p

if __debug__:
    try:
        from typing import Dict, List  # noqa: F401
        from typing_extensions import Literal  # noqa: F401
        EnumTypeSeedRequestType = Literal[0, 1, 2]
    except ImportError:
        pass


class BixinSeedOperate(p.MessageType):
    MESSAGE_WIRE_TYPE = 901

    def __init__(
        self,
        type: EnumTypeSeedRequestType = None,
        seed_importData: str = None,
    ) -> None:
        self.type = type
        self.seed_importData = seed_importData

    @classmethod
    def get_fields(cls) -> Dict:
        return {
            1: ('type', p.EnumType("SeedRequestType", (0, 1, 2)), 0),  # required
            2: ('seed_importData', p.UnicodeType, 0),
        }
