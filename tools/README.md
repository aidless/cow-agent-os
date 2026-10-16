# tools/ — vendored third-party trees moved upstream

The third-party project trees that used to live under this directory were removed so
this workspace reads as its own work. Nothing in this repository imported or called
into them.

They are other people's projects, and each keeps its own license held by its own
authors — fetch them from their own sources:

| was here | upstream |
|---|---|
| `AionUi/` | https://github.com/iOfficeAI/AionUi |
| `AutoResearchClaw-main/` | https://github.com/aiming-lab/AutoResearchClaw |
| `Awesome-Hacking/` | https://github.com/Hack-with-Github/Awesome-Hacking |
| `ECC/` | https://github.com/affaan-m/ECC |
| `TrendRadar-master/` | https://github.com/sansan0/TrendRadar |

Two of these had been unpacked as `X-main/X-main` — an archive that contained its own
top-level folder — which is why the old paths appeared doubled.

Upstream names above were read from each tree's own metadata (`Cargo.toml`,
`README.md`) or from the project's public sources, not inferred from the folder name.
For `ECC`, some of its own documentation also writes the repository as
`affaan-m/everything-claude-code`.
