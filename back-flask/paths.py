from pathlib import Path

import rootpath

ROOT = Path(rootpath.detect(pattern='.gitignore')) # sets ROOT to repository root directory (i.e. directory where .gitignore is in)

GOOGLE_CLOUD_PLATFORMS_API_KEY_FILE = ROOT / 'google_cloud_platforms_api_key.txt'
