# islandora_workbench_lite

This patch for Islandora Workbench corresponds to commit ID 1f6051b6c2c1b60aa588e4c4f3478f4428d5fda9

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
git checkout 1f6051b6c2c1b60aa588e4c4f3478f4428d5fda9
```

Get the `create_media` patch
```bash
wget https://raw.githubusercontent.com/digitalutsc/islandora_workbench_lite/2023/create_media.patch
```

Apply the patch
```bash
git apply --ignore-space-change < create_media.patch
```



