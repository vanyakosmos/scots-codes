from __future__ import annotations

from enum import IntEnum


class ScotsCode(IntEnum):
    description: str

    def __new__(cls, value: int, description: str = "") -> ScotsCode:
        obj = int.__new__(cls, value)
        obj._value_ = value
        obj.description = description
        return obj

    @property
    def phrase(self) -> str:
        """Alias for ``description`` to match ``http.HTTPStatus.phrase``."""
        return self.description

    @property
    def is_informational(self) -> bool:
        return 100 <= self.value <= 199

    @property
    def is_success(self) -> bool:
        return 200 <= self.value <= 299

    @property
    def is_redirection(self) -> bool:
        return 300 <= self.value <= 399

    @property
    def is_client_error(self) -> bool:
        return 400 <= self.value <= 499

    @property
    def is_server_error(self) -> bool:
        return 500 <= self.value <= 599

    @classmethod
    def from_code(cls, code: int) -> ScotsCode | None:
        try:
            return cls(code)
        except ValueError:
            return None

    # 1xx Informational
    AYE_ON_YE_GO = (100, "AYE ON YE GO")
    RIGHT_WERE_SWAPPIN = (101, "RIGHT WE'RE SWAPPIN")
    AYE_HAUD_ON = (102, "AYE HAUD ON")
    HERES_A_WEE_CLUE = (103, "HERE'S A WEE CLUE")

    # 2xx Success
    NAE_BOTHER = (200, "NAE BOTHER")
    THATS_IT_MADE = (201, "THAT'S IT MADE")
    AYE_AHLL_SEE_TAE_IT = (202, "AYE AH'LL SEE TAE IT")
    DINNAE_QUOTE_ME = (203, "DINNAE QUOTE ME")
    HEHAW = (204, "HEHAW")
    CLEAR_THAT_AFF_AN_START_AGAIN = (205, "CLEAR THAT AFF AN START AGAIN")
    HERES_A_WEE_BIT = (206, "HERE'S A WEE BIT")
    BIT_O_THIS_BIT_O_THAT = (207, "BIT O THIS BIT O THAT")
    AH_TELT_YE_AWREADY_YA_WEE_SCUNNER = (208, "AH TELT YE AWREADY YA WEE SCUNNER")
    HERES_WHITS_CHANGED = (226, "HERE'S WHIT'S CHANGED")

    # 3xx Redirection
    TAKE_YER_PICK = (300, "TAKE YER PICK")
    WEVE_FLITTED = (301, "WE'VE FLITTED")
    WERE_OWER_THERE_THE_NOO = (302, "WE'RE OWER THERE THE NOO")
    ASK_HIM_OWER_THERE = (303, "ASK HIM OWER THERE")
    SAME_AULD_SHITE = (304, "SAME AULD SHITE")
    GO_THROUGH_HIM = (305, "GO THROUGH HIM")
    NAE_USE_TAE_ANYBODY = (306, "NAE USE TAE ANYBODY")
    FUCK_OFF_OWER_THERE_FOR_NOO = (307, "FUCK OFF OWER THERE FOR NOO")
    FUCK_OFF_OWER_THERE_FOR_GUID = (308, "FUCK OFF OWER THERE FOR GUID")

    # 4xx Client Error
    WHIT_THE_FUCKS_THIS = (400, "WHIT THE FUCK'S THIS")
    WHO_THE_FUCK_ARE_YOU = (401, "WHO THE FUCK ARE YOU")
    GIES_YER_MONEY = (402, "GIE'S YER MONEY")
    GET_TAE_FUCK = (403, "GET TAE FUCK")
    NO_FUCKIN_HERE_PAL = (404, "NO FUCKIN HERE PAL")
    YE_CANNAE_DAE_THAT = (405, "YE CANNAE DAE THAT")
    WEVE_NANE_O_THAT_KIND = (406, "WE'VE NANE O THAT KIND")
    AN_WHOS_YER_PAL = (407, "AN WHO'S YER PAL")
    AHVE_BEEN_STAUNIN_HERE_AGES = (408, "AH'VE BEEN STAUNIN HERE AGES")
    PICK_A_FUCKIN_LANE = (409, "PICK A FUCKIN LANE")
    DEID_AN_BURIED = (410, "DEID AN BURIED")
    HOW_LANG_IS_IT_THEN = (411, "HOW LANG IS IT THEN")
    THATS_NO_WHIT_WE_AGREED = (412, "THAT'S NO WHIT WE AGREED")
    THATS_FUCKIN_MASSIVE = (413, "THAT'S FUCKIN MASSIVE")
    AHM_NO_READIN_ALL_THAT = (414, "AH'M NO READIN ALL THAT")
    NAE_IDEA_WHIT_THAT_IS = (415, "NAE IDEA WHIT THAT IS")
    IT_DISNAE_GO_THAT_FAR = (416, "IT DISNAE GO THAT FAR")
    AYE_YE_WISH = (417, "AYE YE WISH")
    AHM_A_FUCKIN_TEAPOT = (418, "AH'M A FUCKIN TEAPOT")
    WRONG_CUNT = (421, "WRONG CUNT")
    AH_KEN_WHIT_YE_MEAN_BUT_NAW = (422, "AH KEN WHIT YE MEAN BUT NAW")
    ITS_SNIBBED = (423, "IT'S SNIBBED")
    THE_LAST_WAN_WENT_TITS_UP = (424, "THE LAST WAN WENT TITS UP")
    HAUD_YER_HORSES = (425, "HAUD YER HORSES")
    GET_YERSEL_A_NEW_WAN = (426, "GET YERSEL A NEW WAN")
    CHECK_FIRST_YA_CHANCER = (428, "CHECK FIRST YA CHANCER")
    SLOW_DOON = (429, "SLOW DOON")
    TOO_MUCH_PISH = (431, "TOO MUCH PISH")
    AWAY_YE_CLATTY_WEE_BASTARD = (444, "AWAY YE CLATTY WEE BASTARD")
    THE_COUNCIL_SAYS_NAW = (451, "THE COUNCIL SAYS NAW")

    # 5xx Server Error
    AHVE_FUCKED_IT = (500, "AH'VE FUCKED IT")
    AH_DINNAE_DAE_THAT = (501, "AH DINNAE DAE THAT")
    THE_OTHER_BAMPOTS_BROKEN = (502, "THE OTHER BAMPOT'S BROKEN")
    WERE_FUCKIN_SHUT = (503, "WE'RE FUCKIN SHUT")
    THE_BASTARDS_NO_ANSWERIN = (504, "THE BASTARD'S NO ANSWERIN")
    WHIT_FUCKIN_CENTURY_ARE_YE_IN = (505, "WHIT FUCKIN CENTURY ARE YE IN")
    AHM_STAPPIT_FU = (507, "AH'M STAPPIT FU")
    ROUND_AN_ROUND_YA_DAFT_TWAT = (508, "ROUND AN ROUND YA DAFT TWAT")
    YELL_NEED_MAIR_THAN_THAT = (510, "YE'LL NEED MAIR THAN THAT")
    LOG_IN_TAE_THE_WIFI_PAL = (511, "LOG IN TAE THE WIFI PAL")


StatusScode = ScotsCode


def get_scots_description(code: int) -> str | None:
    status = ScotsCode.from_code(code)
    return status.description if status is not None else None
