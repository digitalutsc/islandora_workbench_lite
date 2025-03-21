# islandora_workbench_lite

This patch for Islandora Workbench corresponds to commit ID b38d37e7ec0e606b55e6545b33859708861e533d

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
git checkout 1df2644ba1de4064f868de9564a1515e40afc070
```

Run setup.py script
```bash
sudo python3 setup.py install
```

Get and apply the `create_media` patch
```bash
wget https://raw.githubusercontent.com/digitalutsc/islandora_workbench_lite/2023_nov/create_media.patch
```
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


