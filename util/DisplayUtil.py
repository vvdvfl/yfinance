from flask import render_template_string


def displayHtml(page_title, heading, table_html):
    return render_template_string(f"""
    <html>
        <head>
            <title>{page_title}</title>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
            <style>
                .table-wrapper {{
                    overflow-x: auto;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>{heading}</h1>
                <div class="table-wrapper">
                {table_html}
                 </div>
            </div>
        </body>
    </html>
    """)