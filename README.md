# islandora_workbench_lite

This patch for Islandora Workbench corresponds to commit ID 3373db618c90d9530deb52437573c32d95dcf9c4

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
git checkout 3373db618c90d9530deb52437573c32d95dcf9c4
```

Get and apply the `create_media` patch
```bash
wget https://raw.githubusercontent.com/digitalutsc/islandora_workbench_lite/refs/heads/main/create_media.patch
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

## Troubleshooting and Errors
If you receive the following error while ingesting content,
```
ERROR:root:Workbench could not connect to https://islandora.dev while requesting "https://islandora.dev/entity/entity_form_display/node.islandora_object.default?_format=json".
ERROR:root:HTTPSConnectionPool(host='islandora.dev', port=443): Max retries exceeded with url: /entity/entity_form_display/node.islandora_object.default?_format=json (Caused by SSLError(SSLCertVerificationError(1, '[SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1081)')))
Error: Workbench could not connect to https://islandora.dev while requesting "https://islandora.dev/entity/entity_form_display/node.islandora_object.default?_format=json"
```

Add ```secure_ssl_only: false``` under the ```host: "https://islandora.dev"``` line in both ```create_islandora_object.yml``` and ```create_islandora_media.yml``` to solve the error. This will ignore the SSL certificates.

Reference: [Islandora Workbench Docs](https://mjordan.github.io/islandora_workbench_docs/configuration/#:~:text=to%20HTTP%20redirects.-,secure_ssl_only,-true)

