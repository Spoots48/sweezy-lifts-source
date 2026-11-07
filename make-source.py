#!/usr/bin/env python3
"""Writes Source/source.json — the SideStore/AltStore source for Sweezy Lifts.
Usage: make-source.py <version> <build> <ipa path> [release notes]"""
import json, os, sys, datetime, plistlib

REPO = "Spoots48/sweezy-lifts-source"
RAW = f"https://raw.githubusercontent.com/{REPO}/main"
HERE = os.path.dirname(os.path.abspath(__file__))

version, build, ipa = sys.argv[1], sys.argv[2], sys.argv[3]
notes = sys.argv[4] if len(sys.argv) > 4 else "Updates and fixes."
info = plistlib.load(open(os.path.join(HERE, "..", "iOS", "Info.plist"), "rb"))
privacy = {k: v for k, v in info.items() if k.endswith("UsageDescription")}

path = os.path.join(HERE, "source.json")
old = json.load(open(path)) if os.path.exists(path) else None
versions = old["apps"][0]["versions"] if old else []
versions = [v for v in versions if not (v["version"] == version and v["buildVersion"] == build)]
versions.insert(0, {
    "version": version,
    "buildVersion": build,
    "date": datetime.date.today().isoformat(),
    "localizedDescription": notes,
    "downloadURL": f"https://github.com/{REPO}/releases/download/v{version}-{build}/SweezyLifts.ipa",
    "size": os.path.getsize(ipa),
    "minOSVersion": "18.0",
})

source = {
    "name": "Sweezy Beatz",
    "identifier": "com.sweezybeatz.source",
    "subtitle": "Apps by Sweezy Beatz",
    "description": "Sweezy Lifts — the cut plan, the workouts and Vee.",
    "iconURL": f"{RAW}/icon.png",
    "website": f"https://github.com/{REPO}",
    "tintColor": "FF8D4C",
    "apps": [{
        "name": "Sweezy Lifts",
        "bundleIdentifier": "com.sweezybeatz.lifts",
        "developerName": "Sweezy Beatz",
        "subtitle": "Your cut, your lifts, and Vee.",
        "localizedDescription": "Track the 11-week cut from 169 to 160: the Push · Pull · Legs · Upper · Lower split with a workout player and rest timer, the meal plan and recipes, daily weigh-ins against the roadmap, photo check-ins with an on-device taper reading, the Journey, optional Apple Watch data, and Vee the dragon cheering you on. Backs up to a folder you choose so a reinstall never loses your progress.",
        "iconURL": f"{RAW}/icon.png",
        "tintColor": "FF8D4C",
        "category": "lifestyle",
        "screenshots": [f"{RAW}/screenshots/{n}" for n in sorted(os.listdir(os.path.join(HERE, "screenshots"))) if n.endswith(".png")],
        "versions": versions,
        "appPermissions": {
            "entitlements": ["com.apple.developer.healthkit", "com.apple.developer.healthkit.access"],
            "privacy": privacy,
        },
    }],
    "news": [],
}
json.dump(source, open(path, "w"), indent=2, ensure_ascii=False)
print(f"source.json · v{version} ({build}) · {os.path.getsize(ipa) // 1024} KB")
