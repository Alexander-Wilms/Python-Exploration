import subprocess

import requests

metainfo_urls = [
    "https://raw.githubusercontent.com/vcmi/vcmi/develop/launcher/eu.vcmi.VCMI.metainfo.xml",
    "https://raw.githubusercontent.com/texstudio-org/texstudio/master/utilities/texstudio.metainfo.xml",
    "https://hg.savannah.gnu.org/hgweb/octave/raw-file/4751f73c878e/etc/icons/org.octave.Octave.metainfo.xml",
    "https://raw.githubusercontent.com/LibrePCB/LibrePCB/master/share/metainfo/org.librepcb.LibrePCB.metainfo.xml",
    "https://projects.blender.org/blender/blender/raw/branch/main/release/freedesktop/org.blender.Blender.metainfo.xml",
    "https://raw.githubusercontent.com/gramps-project/gramps/master/data/org.gramps_project.Gramps.metainfo.xml.in",
]

for metainfo_url in metainfo_urls:
    response = requests.get(metainfo_url)
    filename = metainfo_url.split("/")[-1]
    print(f"ℹ️   ./{filename}:")
    with open(filename, "w") as f:
        f.write(response.text)
    output = subprocess.run(["appstreamcli", "validate", "--pedantic", "--explain", filename], text=True, capture_output=True)
    print(output.stdout)
