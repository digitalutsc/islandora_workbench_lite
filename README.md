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

Clone this repo
```bash
git clone https://github.com/digitalutsc/islandora_workbench_lite.git
```

Change into the Islandora Workbench Lite directory
```bash
cd islandora_workbench_lite
```

Switch to the 2023 branch
```bash
git checkout 2023
```

Switch back to the Islandora Workbench Directory
```bash
cd ..
```

Apply the patch
```bash
git apply < islandora_workbench_lite/create_media.patch
```



