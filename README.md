# islandora_workbench_lite

This patch for Islandora Workbench corresponds to commit ID 520f81220e65e69ade197f85dcc6f1d437df2440

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
git checkout 520f81220e65e69ade197f85dcc6f1d437df2440
```

Run setup.py script
```bash
sudo python3 setup.py install
```

Get and apply the `create_media` patch
```bash
wget https://raw.githubusercontent.com/Kxka/islandora_workbench_lite/rebase/create_media.patch```
```bash
git apply --ignore-space-change < create_media.patch
```

Get and apply the `parent_id` patch

```bash
wget https://raw.githubusercontent.com/digitalutsc/islandora_workbench_lite/2023_nov/parent_id.patch
```

```bash
git apply < parent_id.patch
```


