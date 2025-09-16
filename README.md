# islandora_workbench_lite

This patch for Islandora Workbench corresponds to commit ID 0b058a6ca8f6807f18de24c2dd2c82f3d831a6eb

## Instalation 

Follow the steps in [the islandora_workbench](https://mjordan.github.io/islandora_workbench_docs/installation/)

## Usage
Clone Islandora Workbench
```bash
git clone https://github.com/mjordan/islandora_workbench
```

Change into the Islandora Workbench directory
```bash
cd islandora_workbench
```

Switch the commit ID to the one corresponding to this patch
```bash
git checkout 0b058a6ca8f6807f18de24c2dd2c82f3d831a6eb
```

Get and apply the `create_media` patch
```bash
wget https://raw.githubusercontent.com/Kxka/islandora_workbench_lite/rebase/create_media.patch
```

bash
```
git apply --ignore-space-change < create_media.patch
```

Get and apply the `parent_id` patch

```bash
wget https://raw.githubusercontent.com/digitalutsc/islandora_workbench_lite/refs/heads/main/parent_id.patch
```

```bash
git apply < parent_id.patch
```


