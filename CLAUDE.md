# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository purpose

This repository stores source rule definitions for Clash/Mihomo and sing-box, plus the compiled binary artifacts published from them.

The source-of-truth files live under `*/src/mihomo/*.yaml` and `*/src/singbox/*.json`. Compiled outputs are written to the rule-set directory root as `*.mrs` and `*.srs`.

## Development workflow

There is no local app, package manager, or test suite in this repository. The main workflow is:

1. Edit source rule files.
2. Validate them locally when useful.
3. Commit and push.
4. GitHub Actions recompiles binary artifacts and commits any changed `*.mrs` / `*.srs` files back to `main`.

Primary CI workflow: `.github/workflows/compile.yml`

## Common commands

### Validate and inspect source files

Validate a sing-box source file as JSON:

```bash
python -m json.tool emby/src/singbox/emby.json
```

Inspect the current source files:

```bash
ls emby/src/mihomo
ls emby/src/singbox
```

### Reproduce CI compilation locally

The repo does not include helper scripts; local compilation mirrors `.github/workflows/compile.yml`.

Download Mihomo and compile one rule set:

```bash
MIHOMO_VERSION=1.18.10
wget -q "https://github.com/MetaCubeX/mihomo/releases/download/v${MIHOMO_VERSION}/mihomo-linux-amd64-v${MIHOMO_VERSION}.gz"
gzip -d "mihomo-linux-amd64-v${MIHOMO_VERSION}.gz"
chmod +x "mihomo-linux-amd64-v${MIHOMO_VERSION}"
mv "mihomo-linux-amd64-v${MIHOMO_VERSION}" mihomo
./mihomo convert-ruleset domain yaml emby/src/mihomo/emby.yaml emby/emby.mrs
```

Compile an IP-based Mihomo file (the CI uses `ipcidr` when the filename contains `-ip`):

```bash
./mihomo convert-ruleset ipcidr yaml <group>/src/mihomo/<name>-ip.yaml <group>/<name>-ip.mrs
```

Download sing-box and compile one rule set:

```bash
SINGBOX_VERSION=1.10.7
wget -q "https://github.com/SagerNet/sing-box/releases/download/v${SINGBOX_VERSION}/sing-box-${SINGBOX_VERSION}-linux-amd64.tar.gz"
tar -xzf "sing-box-${SINGBOX_VERSION}-linux-amd64.tar.gz"
mv "sing-box-${SINGBOX_VERSION}-linux-amd64/sing-box" sing-box
chmod +x sing-box
./sing-box rule-set compile emby/src/singbox/emby.json -o emby/emby.srs
```

Re-run the same loops as CI for all rule sets:

```bash
for file in $(find . -path '*/src/mihomo/*.yaml'); do
  name=$(basename "$file" .yaml)
  outdir=$(dirname "$(dirname "$(dirname "$file")")")
  if [[ "$name" == *"-ip"* ]]; then
    type="ipcidr"
  else
    type="domain"
  fi
  ./mihomo convert-ruleset "$type" yaml "$file" "$outdir/$name.mrs"
done

for file in $(find . -path '*/src/singbox/*.json'); do
  name=$(basename "$file" .json)
  outdir=$(dirname "$(dirname "$(dirname "$file")")")
  ./sing-box rule-set compile "$file" -o "$outdir/$name.srs"
done
```

## High-level architecture

### Source vs generated files

The repository is organized by rule-set group, such as `emby/`.

For each group:

- `src/mihomo/*.yaml` contains Mihomo source rules.
- `src/singbox/*.json` contains sing-box source rules.
- `<group>/*.mrs` is generated Mihomo output.
- `<group>/*.srs` is generated sing-box output.

When changing rules, edit the source files rather than generated artifacts unless the task is specifically about compiled outputs.

### Compilation model

The compile job is path-driven rather than hardcoded per rule set:

- any `*/src/mihomo/*.yaml` file becomes a sibling `*.mrs`
- any `*/src/singbox/*.json` file becomes a sibling `*.srs`

That means adding a new rule set usually only requires creating the expected directory structure and source file names; CI discovers it automatically.

### Mihomo vs sing-box rule capabilities

The two source formats are intentionally not symmetric.

Mihomo YAML is constrained by the MRS output format:

- plain entries are exact `DOMAIN` matches
- entries prefixed with `+.` are `DOMAIN-SUFFIX` matches
- MRS does not support `DOMAIN-KEYWORD` or `DOMAIN-REGEX`
- Mihomo source file naming affects compile behavior: filenames containing `-ip` are compiled as `ipcidr`, otherwise `domain`
- domain and IP rules must live in separate Mihomo files because each MRS file is compiled as a single behavior

sing-box JSON is more expressive:

- rule type is encoded in JSON fields like `domain`, `domain_suffix`, `domain_keyword`, `domain_regex`, and `ip_cidr`
- file names do not determine behavior
- one JSON file may mix domain and IP rules and still compile into a single `.srs`
- the repository currently uses sing-box rule-set `version: 2`

### Cross-file maintenance implication

The Mihomo and sing-box sources may intentionally differ because sing-box supports rule types that Mihomo cannot express. Do not assume the two source files should be kept textually identical.

In the current `emby` rule set, `emby/src/singbox/emby.json` includes `domain_keyword` rules that cannot be represented in `emby/src/mihomo/emby.yaml`.

## Repository references

- Overview and usage examples: `README.md`
- Mihomo format details and naming rules: `docs/mihomo.md`
- sing-box format details and rule-set versioning: `docs/singbox.md`

## Notes for future edits

Prefer verifying changes against `.github/workflows/compile.yml` when altering naming, directory layout, or expectations about generated outputs, because CI behavior is defined there.
