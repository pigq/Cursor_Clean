from _utils import *

print(
    f"""
{RED}<== {PURPLE}[{RESET}Cursor Shadow Patch{PURPLE}]{RED} ==>{RESET}

- Custom machine id, mac address, etc."""
)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

if SYSTEM == "Linux":
    appimage = appimagepath(
        input(f"\n{PURPLE}Enter AppImage path: {RESET}(leave blank = auto detect) ")
    )
    appimage_unpacked = appimage_unpack(appimage)
    js = jspath(appimage_detect_jspath(appimage_unpacked))
else:
    appimage = appimage_unpacked = None
    js = jspath(
        input(f"\n{PURPLE}Enter main.js path: {RESET}(leave blank = auto detect) ")
    )
data = load(js)

machineid = randomuuid(
    input(f"\n{PURPLE}MachineId: {RESET}(leave blank = random uuid) ")
)
# async function machineId(returnRaw) {
#     let machineid = processOutput(execSync(commands[PLATFORM], { timeout: 5e3 }).toString()),
#         hash;
#     try {
#         hash = (await import("crypto")).createHash("sha256").update(machineid, "utf8").digest("hex");
#     } catch {
#         hash = uuid();
#     }
#     return returnRaw ? machineid : hash;
# }
data = replace(
    data,
    r"=.{0,50}timeout.{0,10}5e3.*?,",
    f'=/*csp1*/"{machineid}"/*1csp*/,',
    r"=/\*csp1\*/.*?/\*1csp\*/,",
)

mac = macaddr(input(f"\n{PURPLE}Mac Address: {RESET}(leave blank = random mac) "))
# function getMacAddress() {
#     const interfaces = networkInterfaces();
#     for (const name in interfaces) {
#         const details = interfaces[name];
#         if (details) {
#             for (const { mac: m } of details) if (isValidMac(m)) return m;
#         }
#     }
#     throw new Error("Unable to retrieve mac address (unexpected format)");
# }
data = replace(
    data,
    r"(function .{0,50}\{).{0,300}Unable to retrieve mac address.*?(\})",
    f'\\1return/*csp2*/"{mac}"/*2csp*/;\\2',
    r"()return/\*csp2\*/.*?/\*2csp\*/;()",
)

sqm = input(f"\n{PURPLE}Windows SQM Id: {RESET}(leave blank = empty) ")
# async function sqmId(errorBind) {
#     if (isWindows) {
#         const reg = await import("@vscode/windows-registry");
#         try {  // REGPATH = "Software\\Microsoft\\SQMClient"
#             return (reg.GetStringRegKey("HKEY_LOCAL_MACHINE", REGPATH, "MachineId") || "");
#         } catch (e) {
#             return errorBind(e), "";
#         }
#     }
#     return "";
# }
data = replace(
    data,
    r'return.{0,50}\.GetStringRegKey.*?HKEY_LOCAL_MACHINE.*?MachineId.*?\|\|.*?""',
    f'return/*csp3*/"{sqm}"/*3csp*/',
    r"return/\*csp3\*/.*?/\*3csp\*/",
)

devid = randomuuid(input(f"\n{PURPLE}devDeviceId: {RESET}(leave blank = random uuid) "))
# async function devDeviceId(errorBind) {
#     try {
#         return await (await import("@vscode/deviceid")).getDeviceId();
#     } catch (e) {
#         return errorBind(e), uuid();
#     }
# }
data = replace(
    data,
    r"return.{0,50}vscode\/deviceid.*?getDeviceId\(\)",
    f'return/*csp4*/"{devid}"/*4csp*/',
    r"return/\*csp4\*/.*?/\*4csp\*/",
)

# Backup and save
backup(js)
save(js, data)

# Pack AppImage for Linux
if SYSTEM == "Linux":
    assert appimage is not None
    assert appimage_unpacked is not None
    backup(appimage)
    appimage_repack(appimage, appimage_unpacked)

pause()
