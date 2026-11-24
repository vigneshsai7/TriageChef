"""Windows artefact checklist - implement / document per docs/ARTEFACTS.md
Artefacts: Prefetch (.pf), Amcache.hve, Shimcache (SYSTEM), SRUM, .evtx, Registry (SAM/SYSTEM/SOFTWARE/NTUSER.DAT), LNK, JumpLists, Browser History, Recycle Bin ($I/$R), RunKeys/Services/Tasks, MFT/USN."""
WINDOWS_ARTEFACTS = ["Prefetch","Amcache","Shimcache","SRUM","Security.evtx","System.evtx","PowerShell Operational.evtx","NTUSER.DAT","SOFTWARE","SYSTEM","SAM","LNK","JumpLists","WebCacheV01.dat","History","$Recycle.Bin"]
