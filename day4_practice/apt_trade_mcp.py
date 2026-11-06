# apt_trade_mcp.py - 국토교통부 아파트 매매 실거래가 조회 MCP 서버
import json
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

from fastmcp import FastMCP

mcp = FastMCP("apt-trade")

API_URL = "https://apis.data.go.kr/1613000/RTMSDataSvcAptTrade/getRTMSDataSvcAptTrade"
API_KEY = "6e730b15a9a605386c301ebe43621e0a2a05f079cb21db4f57535a7d6ca0b11c"

PAGE_SIZE = 1000   # API 한 페이지 최대 행 수
MAX_PAGES = 10     # 한 달 최대 10,000건까지 훑는다
MAX_LIMIT = 100    # 응답으로 돌려줄 최대 건수


def _fetch_page(region_code: str, year_month: str, page: int):
    query = urllib.parse.urlencode({
        "serviceKey": API_KEY,
        "LAWD_CD": region_code,
        "DEAL_YMD": year_month,
        "numOfRows": PAGE_SIZE,
        "pageNo": page,
    })
    with urllib.request.urlopen(f"{API_URL}?{query}", timeout=20) as response:
        root = ET.fromstring(response.read())
    trades = [{
        "apt": item.findtext("aptNm"),
        "dong": item.findtext("umdNm"),
        "price_manwon": int(item.findtext("dealAmount").replace(",", "")),
        "area_m2": float(item.findtext("excluUseAr")),
        "floor": item.findtext("floor"),
        "date": f'{item.findtext("dealYear")}-{int(item.findtext("dealMonth")):02d}-{int(item.findtext("dealDay")):02d}',
        "cancelled": bool((item.findtext("cdealType") or "").strip()),
    } for item in root.findall("body/items/item")]
    return trades, int(root.findtext("body/totalCount") or 0)


def _normalize(text: str) -> str:
    return "".join((text or "").split()).lower()


@mcp.tool()
def apt_trades(
    region_code: str,
    year_month: str,
    limit: int = 20,
    apt_name: str = "",
    sort: str = "price_desc",
    include_cancelled: bool = False,
) -> str:
    """시군구와 계약 연월로 아파트 매매 실거래 내역을 조회한다.

    해당 월의 거래를 전부 가져온 뒤 단지명으로 거르고 정렬해서 상위 limit건을 돌려준다.
    특정 지역의 아파트 매매 가격, 가장 비싼 단지, 특정 단지의 거래 내역이 필요할 때 사용한다.
    전월세, 오피스텔, 연립다세대 거래에는 사용하지 않는다.
    금액 단위는 만원이고, cancelled가 true면 해제된 거래다.

    Args:
        region_code: 시군구 코드 5자리 (예: 서울 종로구 11110, 강남구 11680, 화성시 동탄구 41597)
        year_month: 계약 연월 YYYYMM (예: 202409)
        limit: 돌려줄 개수 (최대 100)
        apt_name: 단지명 일부. 공백·대소문자 무시 부분 일치 (예: "롯데캐슬").
            등기상 단지명이 영문인 경우가 있다 (예: 메타폴리스 → "METAPOLIS").
            결과가 없으면 영문명이나 더 짧은 키워드로 다시 시도한다.
        sort: "price_desc"(가격 높은 순, 기본), "price_asc", "date_desc"(최근 계약 순), "none"(API 순서)
        include_cancelled: true면 해제된 거래도 포함한다 (기본 false)
    """
    try:
        trades, total = _fetch_page(region_code, year_month, 1)
        page = 1
        while len(trades) < total and page < MAX_PAGES:
            page += 1
            more, _ = _fetch_page(region_code, year_month, page)
            if not more:
                break
            trades.extend(more)
    except Exception:
        return "에러: 실거래가 조회에 실패했습니다. 잠시 후 다시 시도하세요."

    if not trades:
        return "거래가 없습니다. region_code(5자리)와 year_month(YYYYMM)를 확인하세요."

    cancelled_count = sum(t["cancelled"] for t in trades)
    matched = trades if include_cancelled else [t for t in trades if not t["cancelled"]]
    if apt_name:
        key = _normalize(apt_name)
        matched = [t for t in matched if key in _normalize(t["apt"])]

    if sort == "price_desc":
        matched.sort(key=lambda t: t["price_manwon"], reverse=True)
    elif sort == "price_asc":
        matched.sort(key=lambda t: t["price_manwon"])
    elif sort == "date_desc":
        matched.sort(key=lambda t: t["date"], reverse=True)

    limit = max(1, min(limit, MAX_LIMIT))
    if apt_name and not matched:
        return (f'"{apt_name}"와 일치하는 단지가 없습니다 (이 달 거래 {len(trades)}건 확인). '
                "등기상 단지명이 영문이거나 다를 수 있으니 영문명이나 더 짧은 키워드로 다시 시도하세요.")
    return json.dumps({
        "total": total,
        "fetched": len(trades),
        "cancelled": cancelled_count,
        "matched": len(matched),
        "returned": min(limit, len(matched)),
        "trades": matched[:limit],
    }, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    if "test" in sys.argv:
        print(apt_trades("11110", "202409", 2))
        print(apt_trades("99999", "202409"))
    else:
        mcp.run()
