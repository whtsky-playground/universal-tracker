export async function onRequestGet(context) {
  const NOTION_KEY = context.env.NOTION_KEY;
  const DATA_SOURCE_ID = "9ac28a84-c975-4267-b29f-6baec463986a";

  if (!NOTION_KEY) {
    return Response.json({ error: "NOTION_KEY not configured" }, { status: 500 });
  }

  try {
    const res = await fetch(
      `https://api.notion.com/v1/data_sources/${DATA_SOURCE_ID}/query`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${NOTION_KEY}`,
          "Notion-Version": "2025-09-03",
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          sorts: [{ property: "日期", direction: "descending" }],
        }),
      }
    );

    if (!res.ok) {
      const err = await res.text();
      return Response.json({ error: "Notion API error", detail: err }, { status: res.status });
    }

    const data = await res.json();
    const records = (data.results || []).map((page) => {
      const props = page.properties || {};

      const titleArr = props["项目"]?.title || [];
      const name = titleArr.map((t) => t.plain_text || "").join("");

      const dateObj = props["日期"]?.date;
      const date = dateObj?.start || "";

      const typeObj = props["类型"]?.select;
      const type = typeObj?.name || "";

      const original = props["原价"]?.number ?? 0;
      const paid = props["实付"]?.number ?? 0;
      const saved = original - paid;

      const noteArr = props["备注"]?.rich_text || [];
      const note = noteArr.map((t) => t.plain_text || "").join("");

      return { name, date, type, original, paid, saved, note };
    });

    return new Response(JSON.stringify(records), {
      headers: {
        "Content-Type": "application/json",
        "Cache-Control": "public, max-age=300",
        "Access-Control-Allow-Origin": "*",
      },
    });
  } catch (e) {
    return Response.json({ error: "Failed to fetch", detail: e.message }, { status: 500 });
  }
}
