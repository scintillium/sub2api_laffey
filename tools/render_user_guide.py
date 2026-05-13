from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "guide" / "USER_GUIDE_CN.md"
TARGET = ROOT / "guide" / "guide_cn.html"


def slugify(text: str, used: dict[str, int]) -> str:
    base = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    if base and not re.fullmatch(r"\d+", base):
        slug = base
    else:
        slug = f"section-{len(used) + 1}"
    count = used.get(slug, 0)
    used[slug] = count + 1
    return slug if count == 0 else f"{slug}-{count}"


def inline(text: str) -> str:
    placeholders: list[str] = []

    def stash(value: str) -> str:
        placeholders.append(value)
        return f"\x00{len(placeholders) - 1}\x00"

    def image_replace(match: re.Match[str]) -> str:
        alt = html.escape(match.group(1), quote=True)
        src = html.escape(match.group(2), quote=True)
        return stash(
            f'<figure><img src="{src}" alt="{alt}"><figcaption>{alt}</figcaption></figure>'
        )

    def link_replace(match: re.Match[str]) -> str:
        label = inline(match.group(1))
        href = html.escape(match.group(2), quote=True)
        return stash(
            f'<a href="{href}" target="_blank" rel="noopener noreferrer">{label}</a>'
        )

    text = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", image_replace, text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_replace, text)
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)

    def restore(match: re.Match[str]) -> str:
        return placeholders[int(match.group(1))]

    return re.sub("\x00(\\d+)\x00", restore, text)


def split_table_row(line: str) -> list[str]:
    cells = line.strip().strip("|").split("|")
    return [cell.strip() for cell in cells]


def flush_paragraph(parts: list[str], out: list[str]) -> None:
    if parts:
        out.append(f"<p>{inline(' '.join(parts))}</p>")
        parts.clear()


def flush_list(items: list[str], out: list[str], ordered: bool) -> None:
    if not items:
        return
    if ordered:
        for number, item in enumerate(items, 1):
            out.append(
                f'<div class="step"><span class="step-number">{number}</span><div>{inline(item)}</div></div>'
            )
    else:
        out.append(
            '<ul class="nice-list">'
            + "".join(f"<li>{inline(item)}</li>" for item in items)
            + "</ul>"
        )
    items.clear()


def flush_rich_list(
    items: list[tuple[str, list[str]]], out: list[str], ordered: bool
) -> None:
    if not items:
        return
    if ordered:
        for number, (first, children) in enumerate(items, 1):
            child_html = "".join(children)
            out.append(
                f'<div class="step"><span class="step-number">{number}</span><div>{inline(first)}{child_html}</div></div>'
            )
    else:
        out.append(
            '<ul class="nice-list">'
            + "".join(f"<li>{inline(first)}{''.join(children)}</li>" for first, children in items)
            + "</ul>"
        )
    items.clear()


def find_code_end(lines: list[str], start: int) -> int:
    i = start + 1
    while i < len(lines):
        if lines[i].rstrip().startswith("```"):
            return i
        i += 1
    return len(lines) - 1


def render_block_fragment(lines: list[str]) -> str:
    body, _ = render_markdown("\n".join(lines))
    return body


def render_markdown(markdown: str) -> tuple[str, list[tuple[int, str, str]]]:
    lines = markdown.splitlines()
    out: list[str] = []
    toc: list[tuple[int, str, str]] = []
    used_ids: dict[str, int] = {}
    paragraph: list[str] = []
    list_items: list[str] = []
    list_ordered = False
    rich_list_items: list[tuple[str, list[str]]] = []
    rich_list_ordered = False
    in_code = False
    code_lang = ""
    code_lines: list[str] = []
    skipping_manual_toc = False
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()

        if in_code:
            if line.startswith("```"):
                lang = html.escape(code_lang, quote=True)
                code = html.escape("\n".join(code_lines))
                out.append(f'<pre><code class="language-{lang}">{code}</code></pre>')
                in_code = False
                code_lang = ""
                code_lines = []
            else:
                code_lines.append(line)
            i += 1
            continue

        if line.startswith("```"):
            flush_paragraph(paragraph, out)
            flush_list(list_items, out, list_ordered)
            flush_rich_list(rich_list_items, out, rich_list_ordered)
            in_code = True
            code_lang = line[3:].strip() or "text"
            i += 1
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            flush_paragraph(paragraph, out)
            flush_list(list_items, out, list_ordered)
            flush_rich_list(rich_list_items, out, rich_list_ordered)
            level = len(heading.group(1))
            text = heading.group(2).strip()
            if level == 2 and text == "目录":
                skipping_manual_toc = True
                i += 1
                continue
            if skipping_manual_toc and level == 2:
                skipping_manual_toc = False
            if skipping_manual_toc:
                i += 1
                continue
            anchor = slugify(text, used_ids)
            if level > 1:
                toc.append((level, anchor, text))
            out.append(f'<h{level} id="{html.escape(anchor, quote=True)}">{inline(text)}</h{level}>')
            i += 1
            continue

        if skipping_manual_toc:
            i += 1
            continue

        if not line.strip():
            flush_paragraph(paragraph, out)
            flush_list(list_items, out, list_ordered)
            flush_rich_list(rich_list_items, out, rich_list_ordered)
            i += 1
            continue

        if line.startswith(">"):
            flush_paragraph(paragraph, out)
            flush_list(list_items, out, list_ordered)
            flush_rich_list(rich_list_items, out, rich_list_ordered)
            quote_parts = []
            while i < len(lines) and lines[i].startswith(">"):
                quote_parts.append(lines[i].lstrip("> ").rstrip())
                i += 1
            out.append(f"<blockquote>{inline(' '.join(quote_parts))}</blockquote>")
            continue

        if line.strip().startswith("|") and i + 1 < len(lines) and re.match(
            r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", lines[i + 1]
        ):
            flush_paragraph(paragraph, out)
            flush_list(list_items, out, list_ordered)
            flush_rich_list(rich_list_items, out, rich_list_ordered)
            headers = split_table_row(line)
            i += 2
            rows: list[list[str]] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_table_row(lines[i]))
                i += 1
            table = ['<div class="table-wrap"><table><thead><tr>']
            table.extend(f"<th>{inline(cell)}</th>" for cell in headers)
            table.append("</tr></thead><tbody>")
            for row in rows:
                table.append("<tr>")
                table.extend(f"<td>{inline(cell)}</td>" for cell in row)
                table.append("</tr>")
            table.append("</tbody></table></div>")
            out.append("".join(table))
            continue

        ordered = re.match(r"^\s*\d+\.\s+(.+)$", line)
        unordered = re.match(r"^\s*-\s+(.+)$", line)
        if ordered or unordered:
            flush_paragraph(paragraph, out)
            flush_list(list_items, out, list_ordered)
            is_ordered = bool(ordered)
            item = (ordered or unordered).group(1)
            if rich_list_items and rich_list_ordered != is_ordered:
                flush_rich_list(rich_list_items, out, rich_list_ordered)
            rich_list_ordered = is_ordered
            child_lines: list[str] = []
            i += 1
            while i < len(lines):
                next_line = lines[i].rstrip()
                if not next_line.strip():
                    child_lines.append("")
                    i += 1
                    continue
                if next_line.startswith("```"):
                    end = find_code_end(lines, i)
                    child_lines.extend(lines[i : end + 1])
                    i = end + 1
                    continue
                if re.match(r"^\S", next_line) and (
                    re.match(r"^\d+\.\s+", next_line)
                    or re.match(r"^-\s+", next_line)
                    or re.match(r"^#{1,6}\s+", next_line)
                    or next_line.startswith(">")
                    or next_line.startswith("|")
                ):
                    break
                if next_line.startswith("   "):
                    child_lines.append(next_line[3:])
                elif next_line.startswith("\t"):
                    child_lines.append(next_line.lstrip("\t"))
                else:
                    child_lines.append(next_line)
                i += 1
            fragment = render_block_fragment(child_lines).strip() if child_lines else ""
            rich_list_items.append((item, [fragment]))
            continue

        if re.match(r"^\s*!\[", line):
            flush_paragraph(paragraph, out)
            flush_list(list_items, out, list_ordered)
            flush_rich_list(rich_list_items, out, rich_list_ordered)
            out.append(f"<p>{inline(line.strip())}</p>")
            i += 1
            continue

        paragraph.append(line.strip())
        i += 1

    flush_paragraph(paragraph, out)
    flush_list(list_items, out, list_ordered)
    flush_rich_list(rich_list_items, out, rich_list_ordered)
    return "\n".join(out), toc


def render_page(body: str, toc: list[tuple[int, str, str]]) -> str:
    nav = "\n".join(
        f'<a class="toc-level-{level}" href="#{html.escape(anchor, quote=True)}">{html.escape(text)}</a>'
        for level, anchor, text in toc
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Laffey API 使用文档</title>
  <style>
    :root {{ --bg: #f6f7f9; --panel: #ffffff; --text: #17202a; --muted: #607086; --line: #dfe5ec; --accent: #0f766e; --accent-soft: #e7f5f2; --code-bg: #111827; --code-text: #e5e7eb; --shadow: 0 16px 42px rgba(15, 23, 42, 0.08); }}
    * {{ box-sizing: border-box; }} html {{ scroll-behavior: smooth; }}
    body {{ margin: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", "PingFang SC", sans-serif; color: var(--text); background: var(--bg); line-height: 1.72; }}
    a {{ color: var(--accent); text-decoration: none; }} a:hover {{ text-decoration: underline; }}
    .layout {{ display: grid; grid-template-columns: 300px minmax(0, 1fr); min-height: 100vh; }}
    .sidebar {{ position: sticky; top: 0; height: 100vh; overflow-y: auto; padding: 28px 18px; background: #fff; border-right: 1px solid var(--line); }}
    .sidebar h2 {{ margin: 0 0 16px; font-size: 18px; }} .toc {{ display: flex; flex-direction: column; gap: 2px; }}
    .toc a {{ display: block; border-radius: 8px; padding: 7px 10px; color: #334155; font-size: 14px; line-height: 1.45; }}
    .toc a:hover {{ background: var(--accent-soft); color: #0f4f49; text-decoration: none; }}
    .toc-level-3 {{ padding-left: 22px !important; font-size: 13px !important; color: #526276 !important; }} .toc-level-4 {{ padding-left: 34px !important; font-size: 12px !important; color: #64748b !important; }} .toc-level-5 {{ padding-left: 46px !important; font-size: 12px !important; color: #77859a !important; }}
    .content {{ padding: 42px min(7vw, 92px); }} article {{ max-width: 980px; margin: 0 auto; background: var(--panel); border: 1px solid var(--line); border-radius: 12px; box-shadow: var(--shadow); padding: 44px min(6vw, 68px); }}
    h1, h2, h3, h4, h5, h6 {{ line-height: 1.35; scroll-margin-top: 24px; }} h1 {{ margin: 0 0 26px; font-size: 34px; }} h2 {{ margin: 44px 0 16px; padding-top: 12px; border-top: 1px solid var(--line); font-size: 26px; }} h3 {{ margin: 30px 0 12px; font-size: 21px; }} h4 {{ margin: 24px 0 10px; font-size: 17px; }} h5 {{ margin: 20px 0 8px; font-size: 15px; }}
    p {{ margin: 12px 0; }} strong {{ font-weight: 700; }} code {{ padding: 2px 6px; border-radius: 6px; background: #eef2f7; font-family: Consolas, "SFMono-Regular", Menlo, monospace; font-size: 0.92em; }} pre {{ position: relative; margin: 16px 0; padding: 46px 18px 16px; overflow: auto; border-radius: 10px; background: var(--code-bg); }} pre code {{ padding: 0; background: transparent; color: var(--code-text); font-size: 14px; }}
    .copy-code-button {{ position: absolute; top: 10px; right: 10px; border: 1px solid rgba(229, 231, 235, 0.22); border-radius: 7px; padding: 5px 10px; background: rgba(255, 255, 255, 0.08); color: var(--code-text); font: 12px/1.2 -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", "PingFang SC", sans-serif; cursor: pointer; transition: background 0.15s ease, border-color 0.15s ease, color 0.15s ease; }}
    .copy-code-button:hover, .copy-code-button:focus-visible {{ background: rgba(255, 255, 255, 0.16); border-color: rgba(229, 231, 235, 0.42); outline: none; }}
    .copy-code-button.is-copied {{ border-color: rgba(20, 184, 166, 0.55); color: #99f6e4; }}
    blockquote {{ margin: 16px 0; padding: 12px 16px; border-left: 4px solid var(--accent); background: var(--accent-soft); color: #24413f; border-radius: 0 8px 8px 0; }} .nice-list {{ padding-left: 22px; margin: 12px 0 18px; }} .nice-list li {{ margin: 6px 0; }}
    .step {{ display: grid; grid-template-columns: 30px minmax(0, 1fr); gap: 10px; align-items: start; margin: 10px 0; }} .step-number {{ display: inline-grid; place-items: center; width: 26px; height: 26px; border-radius: 50%; background: var(--accent); color: white; font-size: 13px; font-weight: 700; line-height: 1; }}
    figure {{ margin: 18px 0 24px; border: 1px solid var(--line); border-radius: 10px; overflow: hidden; background: #f8fafc; }} figure img {{ display: block; width: 100%; height: auto; }} figcaption {{ padding: 8px 12px; color: var(--muted); font-size: 13px; border-top: 1px solid var(--line); }}
    .table-wrap {{ overflow-x: auto; margin: 16px 0 22px; border: 1px solid var(--line); border-radius: 10px; }} table {{ width: 100%; border-collapse: collapse; min-width: 620px; }} th, td {{ padding: 11px 13px; border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }} th {{ background: #f1f5f9; font-weight: 700; }} tr:last-child td {{ border-bottom: 0; }}
    @media (max-width: 900px) {{ .layout {{ display: block; }} .sidebar {{ position: relative; height: auto; max-height: 45vh; border-right: 0; border-bottom: 1px solid var(--line); }} .content {{ padding: 22px 14px; }} article {{ padding: 28px 18px; border-radius: 10px; }} h1 {{ font-size: 28px; }} h2 {{ font-size: 23px; }} }}
  </style>
</head>
<body>
  <div class="layout">
    <aside class="sidebar">
      <h2>目录</h2>
      <nav class="toc" aria-label="页面目录">
{nav}
      </nav>
    </aside>
    <main class="content"><article>
{body}
    </article></main>
  </div>
  <script>
    (function () {{
      function copyText(text) {{
        if (navigator.clipboard && window.isSecureContext) {{
          return navigator.clipboard.writeText(text);
        }}

        var textarea = document.createElement("textarea");
        textarea.value = text;
        textarea.setAttribute("readonly", "");
        textarea.style.position = "fixed";
        textarea.style.top = "-9999px";
        document.body.appendChild(textarea);
        textarea.select();

        try {{
          document.execCommand("copy");
          return Promise.resolve();
        }} catch (error) {{
          return Promise.reject(error);
        }} finally {{
          document.body.removeChild(textarea);
        }}
      }}

      document.querySelectorAll("pre").forEach(function (block) {{
        if (block.querySelector(".copy-code-button")) {{
          return;
        }}

        var button = document.createElement("button");
        button.type = "button";
        button.className = "copy-code-button";
        button.textContent = "复制";
        button.setAttribute("aria-label", "复制代码");

        button.addEventListener("click", function () {{
          var code = block.querySelector("code");
          var text = code ? code.innerText : block.innerText;

          copyText(text).then(function () {{
            button.textContent = "已复制";
            button.classList.add("is-copied");
            window.setTimeout(function () {{
              button.textContent = "复制";
              button.classList.remove("is-copied");
            }}, 1600);
          }}).catch(function () {{
            button.textContent = "复制失败";
            window.setTimeout(function () {{
              button.textContent = "复制";
            }}, 1600);
          }});
        }});

        block.appendChild(button);
      }});
    }}());
  </script>
</body>
</html>
"""


def main() -> None:
    body, toc = render_markdown(SOURCE.read_text(encoding="utf-8"))
    TARGET.write_text(render_page(body, toc), encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
