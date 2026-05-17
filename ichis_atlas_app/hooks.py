app_name = "ichis_atlas_app"
app_title = "GF Atlas"
app_publisher = "GREENFARMS"
app_description = "GREENFARMS Corporate Foundation — Estrutura organizacional corporativa"
app_email = "flexfernandes@gmail.com"
app_license = "mit"
app_version = "1.0.0"

after_install = "ichis_atlas_app.install.after_install"

fixtures = [
    {
        "dt": "Role",
        "filters": [["name", "in", ["GF Manager", "GF Editor", "GF Viewer"]]]
    }
]
