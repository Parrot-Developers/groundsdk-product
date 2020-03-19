
ANDROID_COMMON_CONFIG_DIR := $(call my-dir)

# Include common product.mk
include $(ANDROID_COMMON_CONFIG_DIR)/../../common/config/product.mk

# use global config for all variantes
CONFIG_GLOBAL_FILE := $(ANDROID_COMMON_CONFIG_DIR)/global.config

# Setup TARGET_OS
TARGET_OS := linux
TARGET_OS_FLAVOUR := android
TARGET_LIBC := bionic
TARGET_FORCE_STATIC := 1
TARGET_USE_CLANG := 1

TARGET_ANDROID_APILEVEL := 24
TARGET_ANDROID_STL := libc++
TARGET_ANDROID_SHARED_STL := 1

# Setup arch/cpu based on abi
ifeq ("$(ANDROID_ABI)","armeabi")
  TARGET_ARCH := arm
else ifeq ("$(ANDROID_ABI)","armeabi-v7a")
  TARGET_ARCH := arm
  TARGET_CPU := armv7a
else ifeq ("$(ANDROID_ABI)","mips")
  TARGET_ARCH := mips
  TARGET_CPU :=
else ifeq ("$(ANDROID_ABI)","x86")
  TARGET_ARCH := x86
  TARGET_CPU :=
else ifeq ("$(ANDROID_ABI)","arm64-v8a")
  TARGET_ARCH := aarch64
  TARGET_CPU :=
else ifeq ("$(ANDROID_ABI)","mips64")
  TARGET_ARCH := mips64
  TARGET_CPU :=
else ifeq ("$(ANDROID_ABI)","x86_64")
  TARGET_ARCH := x64
  TARGET_CPU :=
else ifeq ("$(ANDROID_ABI)","")
  $(warning Missing ANDROID_ABI using armeabi-v7a)
  TARGET_ARCH := arm
  TARGET_CPU := armv7a
else
  $(error Invalid ANDROID_ABI: $(ANDROID_ABI))
endif

ifndef ANDROID_NDK_PATH
  $(error Missing ANDROID_NDK_PATH)
endif

ifndef ANDROID_SDK_PATH
  $(error Missing ANDROID_SDK_PATH)
endif

TARGET_ANDROID_NDK := $(ANDROID_NDK_PATH)
TARGET_ANDROID_SDK := $(ANDROID_SDK_PATH)

TARGET_DEFAULT_LIB_DESTDIR := usr/lib
