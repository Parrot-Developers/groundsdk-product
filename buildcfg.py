import os
import dragon
import shutil
import types

import apps_tools.android as android
import apps_tools.ios as ios

#===============================================================================
# Android
#===============================================================================

gsdk = types.SimpleNamespace()

if dragon.VARIANT == "android":
    gsdk.android_abis = ['armeabi-v7a', 'arm64-v8a', 'x86', 'x86_64']
    gsdk.gradle_path = os.path.join(dragon.VARIANT_DIR, 'gradle')
    gsdk.package_path = os.path.join(
        dragon.WORKSPACE_DIR, 'packages', 'groundsdk-android')

    sdkcore_jni_path = os.path.join(
        gsdk.package_path, 'sdkcore', 'src', 'main', 'jni')

    # Supported NDKs : from r17b to r18 excluded
    android.check_ndk_version(min_version="r17b", max_version="r18")

    android.add_task_build_common(gsdk.android_abis)

    android.add_ndk_build_task(
        name="build-jni",
        desc="Build android common code & groundsdk jni",
        subtasks=["build-common"],
        calldir=sdkcore_jni_path,
        module="sdkcore",
        abis=gsdk.android_abis
    )

    android.add_ndk_build_task(
        name="build-jni-nodep",
        desc="Build android groundsdk jni only",
        calldir=sdkcore_jni_path,
        module="sdkcore",
        abis=gsdk.android_abis
    )

    android.add_ndk_build_task(
        name="clean-jni",
        desc="Clean android groundsdk jni",
        calldir=sdkcore_jni_path,
        module="sdkcore",
        abis=gsdk.android_abis,
        extra_args=["clean"],
        ignore_failure=True
    )

    android.add_gradle_task(
        name="build",
        desc="Build android groundsdk with tests and demo app",
        subtasks=["build-jni"],
        calldir=gsdk.gradle_path,
        target="build",
        abis=gsdk.android_abis
    )

    android.add_gradle_task(
        name="clean",
        desc="Clean android groundsdk",
        subtasks=["clean-jni", "clean-common"],
        calldir=gsdk.gradle_path,
        target="clean",
        abis=gsdk.android_abis
    )

    android.add_gradle_task(
        name="test",
        desc="Run all tests",
        subtasks=["build-jni"],
        calldir=gsdk.gradle_path,
        target="build",
        abis=gsdk.android_abis,
        extra_args=["connectedCheck"]
    )

    android.add_gradle_task(
        name="doc",
        desc="Build GroundSdk API documentation",
        calldir=gsdk.gradle_path,
        target="groundsdk:doc",
        abis=gsdk.android_abis
    )

#===============================================================================
# iOS
#===============================================================================

if dragon.VARIANT == "ios" or dragon.VARIANT == "ios_sim":
    gsdk.xcode_path = os.path.join(dragon.PRODUCT_DIR, 'ios', 'xcode')

    ios.add_task_build_common()

    ios.add_xcodebuild_task(
        name="build-nodep",
        desc="build all ground sdk projects including tests and demo in "\
        "debug mode. without dependencies",
        calldir=gsdk.xcode_path,
        workspace="groundsdk.xcworkspace",
        configuration="Debug",
        scheme="All",
        action="build"
    )

    ios.add_xcodebuild_task(
        name="analyze",
        desc="run analayzer on all projects",
        subtasks=["build-common"],
        calldir=gsdk.xcode_path,
        workspace="groundsdk.xcworkspace",
        configuration="Debug",
        scheme="All",
        action="analyze"
    )

    ios.add_xcodebuild_task(
        name="analyze-nodep",
        desc="run analayzer on all projects, without dependencies",
        calldir=gsdk.xcode_path,
        workspace="groundsdk.xcworkspace",
        configuration="Debug",
        scheme="All",
        action="analyze"
    )

    ios.add_jazzy_task(
        name="doc",
        desc="Generate GroundSdk doc",
        subtasks=["build"],
        calldir=os.path.join(dragon.WORKSPACE_DIR,  "packages", "groundsdk-ios",
            "GroundSdk"),
        scheme="GroundSdk"
    )

    ios.add_jazzy_task(
        name="doc-nodep",
        desc="Generate GroundSdk doc, without dependencies",
        calldir=os.path.join(dragon.WORKSPACE_DIR,  "packages", "groundsdk-ios",
            "GroundSdk"),
        scheme="GroundSdk"
    )

    ios.add_xcodebuild_task(
        name="clean",
        desc="clean all ground sdk projects",
        subtasks=["clean-common"],
        calldir=gsdk.xcode_path,
        workspace="groundsdk.xcworkspace",
        configuration="Debug",
        scheme="All",
        action="clean"
    )

if dragon.VARIANT == "ios":

    ios.add_xcodebuild_task(
        name="build",
        desc="build all ground sdk projects",
        subtasks=["build-common"],
        calldir=gsdk.xcode_path,
        workspace="groundsdk.xcworkspace",
        configuration="Debug",
        scheme="All",
        action="build"
    )

elif dragon.VARIANT == "ios_sim":

    ios.add_xcodebuild_task(
        name="build",
        desc="build all ground sdk projects including tests",
        subtasks=["build-common"],
        calldir=gsdk.xcode_path,
        workspace="groundsdk.xcworkspace",
        configuration="Debug",
        scheme="All",
        action="build-for-testing"
    )

    ios.add_xctool_task(
        name="test",
        desc="build all ground sdk projects and run all tests",
        subtasks=["build"],
        calldir=gsdk.xcode_path,
        workspace="groundsdk.xcworkspace",
        configuration="Debug",
        scheme="All",
        action="run-tests",
        reporter="junit:%s" % os.path.join(dragon.OUT_DIR, "test-results.xml"),
    )

    ios.add_xctool_task(
        name="test-nodep",
        desc="build all ground sdk projects and run all tests, without "\
        "dependencies",
        calldir=gsdk.xcode_path,
        workspace="groundsdk.xcworkspace",
        configuration="Debug",
        scheme="All",
        action="run-tests",
        reporter="junit:%s" % os.path.join(dragon.OUT_DIR, "test-results.xml"),
    )

try:
    import private.buildext
    private.buildext.apply(**gsdk.__dict__)
except ImportError:
    pass
