# Decompiled with PyLingual (https://pylingual.io)
# Internal filename: Yay you almost got it
# Bytecode version: 3.10.0rc2 (3439)
# Source timestamp: 1970-01-01 00:00:00 UTC (0)

pass
def main(flag):
    from types import FunctionType
    from copyreg import dispatch_table
    from copyreg import _extension_registry, _inverted_registry, _extension_cache
    from itertools import islice
    from functools import partial
    import sys
    from sys import maxsize
    from struct import pack, unpack
    import re
    import io
    import codecs
    import _compat_pickle
    __all__ = ['PickleError', 'PicklingError', 'UnpicklingError', 'Pickler', 'Unpickler', 'dump', 'dumps', 'load', 'loads']
    _HAVE_PICKLE_BUFFER = False
    bytes_types = (bytes, bytearray)
    format_version = '4.0'
    compatible_formats = ['1.0', '1.1', '1.2', '1.3', '2.0', '3.0', '4.0', '5.0']
    HIGHEST_PROTOCOL = 5
    DEFAULT_PROTOCOL = 4

    class PickleError(Exception):
        pass

    class PicklingError(PickleError):
        pass

    class UnpicklingError(PickleError):
        pass

    class _Stop(Exception):
        def __init__(self, value):
            self.value = value
    MARK = b'('
    STOP = b'.'
    POP = b'0'
    POP_MARK = b'1'
    DUP = b'2'
    FLOAT = b'F'
    INT = b'I'
    BININT = b'J'
    BININT1 = b'K'
    LONG = b'L'
    BININT2 = b'M'
    NONE = b'N'
    PERSID = b'P'
    BINPERSID = b'Q'
    REDUCE = b'R'
    STRING = b'S'
    BINSTRING = b'T'
    SHORT_BINSTRING = b'U'
    UNICODE = b'V'
    BINUNICODE = b'X'
    APPEND = b'a'
    BUILD = b'b'
    GLOBAL = b'c'
    DICT = b'd'
    EMPTY_DICT = b'}'
    APPENDS = b'e'
    GET = b'g'
    BINGET = b'h'
    INST = b'i'
    LONG_BINGET = b'j'
    LIST = b'l'
    EMPTY_LIST = b']'
    OBJ = b'o'
    PUT = b'p'
    BINPUT = b'q'
    LONG_BINPUT = b'r'
    SETITEM = b's'
    TUPLE = b't'
    EMPTY_TUPLE = b')'
    SETITEMS = b'u'
    BINFLOAT = b'G'
    TRUE = b'I01\n'
    FALSE = b'I00\n'
    PROTO = b'\x80'
    NEWOBJ = b'\x81'
    EXT1 = b'\x82'
    EXT2 = b'\x83'
    EXT4 = b'\x84'
    TUPLE1 = b'\x85'
    TUPLE2 = b'\x86'
    TUPLE3 = b'\x87'
    NEWTRUE = b'\x88'
    NEWFALSE = b'\x89'
    LONG1 = b'\x8a'
    LONG4 = b'\x8b'
    _tuplesize2code = [EMPTY_TUPLE, TUPLE1, TUPLE2, TUPLE3]
    BINBYTES = b'B'
    SHORT_BINBYTES = b'C'
    SHORT_BINUNICODE = b'\x8c'
    BINUNICODE8 = b'\x8d'
    BINBYTES8 = b'\x8e'
    EMPTY_SET = b'\x8f'
    ADDITEMS = b'\x90'
    FROZENSET = b'\x91'
    NEWOBJ_EX = b'\x92'
    STACK_GLOBAL = b'\x93'
    MEMOIZE = b'\x94'
    FRAME = b'\x95'
    BYTEARRAY8 = b'\x96'
    NEXT_BUFFER = b'\x97'
    READONLY_BUFFER = b'\x98'
    __all__.extend([x for x in dir() if re.match('[A-Z][A-Z0-9_]+$', x)])

    class _Framer:
        _FRAME_SIZE_MIN = 4
        _FRAME_SIZE_TARGET = 65536

        def __init__(self, file_write):
            self.file_write = file_write
            self.current_frame = None

        def start_framing(self):
            self.current_frame = io.BytesIO()

        def end_framing(self):
            if not self.current_frame or self.current_frame.tell() > 0:
                self.commit_frame(force=True)
                self.current_frame = None

        def commit_frame(self, force=False):
            if self.current_frame:
                f = self.current_frame
                if f.tell() >= self._FRAME_SIZE_TARGET or force:
                    data = f.getbuffer()
                    write = self.file_write
                    if len(data) >= self._FRAME_SIZE_MIN:
                        write(FRAME + pack('<Q', len(data)))
                    write(data)
                    self.current_frame = io.BytesIO()

        def write(self, data):
            if self.current_frame:
                return self.current_frame.write(data)
            return self.file_write(data)

        def write_large_bytes(self, header, payload):
            write = self.file_write
            if self.current_frame:
                self.commit_frame(force=True)
            write(header)
            write(payload)

    class _Unframer:
        def __init__(self, file_read, file_readline, file_tell=None):
            self.file_read = file_read
            self.file_readline = file_readline
            self.current_frame = None

        def readinto(self, buf):
            if self.current_frame:
                n = self.current_frame.readinto(buf)
                if n == 0 and len(buf)!= 0:
                    self.current_frame = None
                    n = len(buf)
                    buf[:] = self.file_read(n)
                    return n
                if n < len(buf):
                    raise UnpicklingError('pickle exhausted before end of frame')
                return n
            n = len(buf)
            buf[:] = self.file_read(n)
            return n

        def read(self, n):
            if self.current_frame:
                data = self.current_frame.read(n)
                if not data and n!= 0:
                    self.current_frame = None
                    return self.file_read(n)
                if len(data) < n:
                    raise UnpicklingError('pickle exhausted before end of frame')
                return data
            return self.file_read(n)

        def readline(self):
            if self.current_frame:
                data = self.current_frame.readline()
                if not data:
                    self.current_frame = None
                    return self.file_readline()
                if data[(-1)]!= 10:
                    raise UnpicklingError('pickle exhausted before end of frame')
                return data
            return self.file_readline()

        def load_frame(self, frame_size):
            if self.current_frame and self.current_frame.read()!= b'':
                raise UnpicklingError('beginning of a new frame before end of current frame')
            self.current_frame = io.BytesIO(self.file_read(frame_size))

    def _getattribute(obj, name):
        top = obj
        for subpath in name.split('.'):
            if subpath == '<locals>':
                raise AttributeError('Can\'t get local attribute {!r} on {!r}'.format(name, top))
            try:
                parent = obj
                obj = getattr(obj, subpath)
            except AttributeError:
                raise AttributeError('Can\'t get attribute {!r} on {!r}'.format(name, top)) from None
        return (obj, parent)

    def whichmodule(obj, name):
        pass
        module_name = getattr(obj, '__module__', None)
        if module_name is not None:
            return module_name
        for module_name, module in sys.modules.copy().items():
            if module_name == '__main__' or module_name == '__mp_main__' or module is None:
                continue
            try:
                if _getattribute(module, name)[0] is obj:
                    return module_name
            except AttributeError:
                continue
        return '__main__'

    def encode_long(x):
        pass
        if x == 0:
            return b''
        nbytes = (x.bit_length() >> 3) + 1
        result = x.to_bytes(nbytes, byteorder='little', signed=True)
        if x < 0 and nbytes > 1 and (result[(-1)] == 255) and (result[(-2)] & 128!= 0):
            result = result[:(-1)]
        return result

    def decode_long(data):
        pass
        return int.from_bytes(data, byteorder='little', signed=True)
    _NoValue = object()

    class _Pickler(*, **FLOAT):
        def __init__(self, file, protocol=None, *, fix_imports=True, buffer_callback=None):
            pass
            if protocol is None:
                protocol = DEFAULT_PROTOCOL
            if protocol < 0:
                protocol = HIGHEST_PROTOCOL
            else:  # inserted
                if not 0 <= protocol <= HIGHEST_PROTOCOL:
                    raise ValueError('pickle protocol must be <= %d' % HIGHEST_PROTOCOL)
            if buffer_callback is not None and protocol < 5:
                raise ValueError('buffer_callback needs protocol >= 5')
            self._buffer_callback = buffer_callback
            try:
                self._file_write = file.write
            except AttributeError:
                raise TypeError('file must have a \'write\' attribute')
            self.framer = _Framer(self._file_write)
            self.write = self.framer.write
            self._write_large_bytes = self.framer.write_large_bytes
            self.memo = {}
            self.proto = int(protocol)
            self.bin = protocol >= 1
            self.fast = 0
            self.fix_imports = fix_imports and protocol < 3

        def clear_memo(self):
            pass
            self.memo.clear()

        def dump(self, obj):
            pass
            if not hasattr(self, '_file_write'):
                raise PicklingError('Pickler.__init__() was not called by %s.__init__()' % (self.__class__.__name__,))
            if self.proto >= 2:
                self.write(PROTO + pack('<B', self.proto))
            if self.proto >= 4:
                self.framer.start_framing()
            self.save(obj)
            self.write(STOP)
            self.framer.end_framing()

        def memoize(self, obj):
            pass
            if self.fast:
                return
            idx = len(self.memo)
            self.write(self.put(idx))
            self.memo[id(obj)] = (idx, obj)

        def put(self, idx):
            if self.proto >= 4:
                return MEMOIZE
            if self.bin:
                if idx < 256:
                    return BINPUT + pack('<B', idx)
                return LONG_BINPUT + pack('<I', idx)
            return PUT + repr(idx).encode('ascii') + b'\n'

        def get(self, i):
            if self.bin:
                if i < 256:
                    return BINGET + pack('<B', i)
                return LONG_BINGET + pack('<I', i)
            return GET + repr(i).encode('ascii') + b'\n'

        def save(self, obj, save_persistent_id=True):
            self.framer.commit_frame()
            if save_persistent_id:
                pid = self.persistent_id(obj)
                if pid is not None:
                    self.save_pers(pid)
                    return
            x = self.memo.get(id(obj))
            if x is not None:
                self.write(self.get(x[0]))
                return
            rv = NotImplemented
            reduce = getattr(self, 'reducer_override', _NoValue)
            if reduce is not _NoValue:
                rv = reduce(obj)
            if rv is NotImplemented:
                t = type(obj)
                f = self.dispatch.get(t)
                if f is not None:
                    f(self, obj)
                    return
                reduce = getattr(self, 'dispatch_table', dispatch_table).get(t, _NoValue)
                if reduce is not _NoValue:
                    rv = reduce(obj)
                else:  # inserted
                    if issubclass(t, type):
                        self.save_global(obj)
                        return
                    reduce = getattr(obj, '__reduce_ex__', _NoValue)
                    if reduce is not _NoValue:
                        rv = reduce(self.proto)
                    else:  # inserted
                        reduce = getattr(obj, '__reduce__', _NoValue)
                        if reduce is not _NoValue:
                            rv = reduce()
                        else:  # inserted
                            raise PicklingError('Can\'t pickle %r object: %r' % (t.__name__, obj))
            if isinstance(rv, str):
                self.save_global(obj, rv)
                return
            if not isinstance(rv, tuple):
                raise PicklingError('%s must return string or tuple' % reduce)
            l = len(rv)
            if not 2 <= l <= 6:
                raise PicklingError('Tuple returned by %s must have two to six elements' % reduce)
            self.save_reduce(*rv, obj=obj)

        def persistent_id(self, obj):
            return

        def save_pers(self, pid):
            if self.bin:
                self.save(pid, save_persistent_id=False)
                self.write(BINPERSID)
            else:  # inserted
                try:
                    self.write(PERSID + str(pid).encode('ascii') + b'\n')
                except UnicodeEncodeError:
                    raise PicklingError('persistent IDs in protocol 0 must be ASCII strings')
        pass
        pass
        def save_reduce(self, func, args, state=None, listitems=None, dictitems=None, state_setter=None, *, obj=None):
            if not isinstance(args, tuple):
                raise PicklingError('args from save_reduce() must be a tuple')
            if not callable(func):
                raise PicklingError('func from save_reduce() must be callable')
            save = self.save
            write = self.write
            func_name = getattr(func, '__name__', '')
            if self.proto >= 2 and func_name == '__newobj_ex__':
                cls, args, kwargs = args
                if not hasattr(cls, '__new__'):
                    raise PicklingError('args[0] from {} args has no __new__'.format(func_name))
                if obj is not None and cls is not obj.__class__:
                    raise PicklingError('args[0] from {} args has the wrong class'.format(func_name))
                if self.proto >= 4:
                    save(cls)
                    save(args)
                    save(kwargs)
                    write(NEWOBJ_EX)
                else:  # inserted
                    func = partial(cls.__new__, cls, *args, **kwargs)
                    save(func)
                    save(())
                    write(REDUCE)
            else:  # inserted
                if self.proto >= 2 and func_name == '__newobj__':
                    cls = args[0]
                    if not hasattr(cls, '__new__'):
                        raise PicklingError('args[0] from __newobj__ args has no __new__')
                    if obj is not None and cls is not obj.__class__:
                        raise PicklingError('args[0] from __newobj__ args has the wrong class')
                    args = args[1:]
                    save(cls)
                    save(args)
                    write(NEWOBJ)
                else:  # inserted
                    save(func)
                    save(args)
                    write(REDUCE)
            if obj is not None:
                if id(obj) in self.memo:
                    write(POP + self.get(self.memo[id(obj)][0]))
                else:  # inserted
                    self.memoize(obj)
            if listitems is not None:
                self._batch_appends(listitems)
            if dictitems is not None:
                self._batch_setitems(dictitems)
            if state is not None:
                if state_setter is None:
                    save(state)
                    write(BUILD)
                else:  # inserted
                    save(state_setter)
                    save(obj)
                    save(state)
                    write(TUPLE2)
                    write(REDUCE)
                    write(POP)
        dispatch = {}

        def save_none(self, obj):
            self.write(NONE)
        dispatch[type(None)] = save_none

        def save_bool(self, obj):
            if self.proto >= 2:
                self.write(NEWTRUE if obj else NEWFALSE)
            else:  # inserted
                self.write(TRUE if obj else FALSE)
        dispatch[bool] = save_bool

        def save_long(self, obj):
            if self.bin:
                if obj >= 0:
                    if obj <= 255:
                        self.write(BININT1 + pack('<B', obj))
                    else:  # inserted
                        if obj <= 65535:
                            self.write(BININT2 + pack('<H', obj))
                if (-2147483648) <= obj <= 2147483647:
                    self.write(BININT + pack('<i', obj))
            if self.proto >= 2:
                encoded = encode_long(obj)
                n = len(encoded)
                if n < 256:
                    self.write(LONG1 + pack('<B', n) + encoded)
                else:  # inserted
                    self.write(LONG4 + pack('<i', n) + encoded)
            else:  # inserted
                if (-2147483648) <= obj <= 2147483647:
                    self.write(INT + repr(obj).encode('ascii') + b'\n')
                else:  # inserted
                    self.write(LONG + repr(obj).encode('ascii') + b'L\n')
        dispatch[int] = save_long

        def save_float(self, obj):
            if self.bin:
                self.write(BINFLOAT + pack('>d', obj))
            else:  # inserted
                self.write(FLOAT + repr(obj).encode('ascii') + b'\n')
        dispatch[float] = save_float

        def _save_bytes_no_memo(self, obj):
            n = len(obj)
            if n <= 255:
                self.write(SHORT_BINBYTES + pack('<B', n) + obj)
            else:  # inserted
                if n > 4294967295 and self.proto >= 4:
                    self._write_large_bytes(BINBYTES8 + pack('<Q', n), obj)
                else:  # inserted
                    if n >= self.framer._FRAME_SIZE_TARGET:
                        self._write_large_bytes(BINBYTES + pack('<I', n), obj)
                    else:  # inserted
                        self.write(BINBYTES + pack('<I', n) + obj)

        def save_bytes(self, obj):
            if self.proto < 3:
                if not obj:
                    self.save_reduce(bytes, (), obj=obj)
                else:  # inserted
                    self.save_reduce(codecs.encode, (str(obj, 'latin1'), 'latin1'), obj=obj)
            else:  # inserted
                self._save_bytes_no_memo(obj)
                self.memoize(obj)
        dispatch[bytes] = save_bytes

        def _save_bytearray_no_memo(self, obj):
            n = len(obj)
            if n >= self.framer._FRAME_SIZE_TARGET:
                self._write_large_bytes(BYTEARRAY8 + pack('<Q', n), obj)
            else:  # inserted
                self.write(BYTEARRAY8 + pack('<Q', n) + obj)

        def save_bytearray(self, obj):
            if self.proto < 5:
                if not obj:
                    self.save_reduce(bytearray, (), obj=obj)
                else:  # inserted
                    self.save_reduce(bytearray, (bytes(obj),), obj=obj)
            else:  # inserted
                self._save_bytearray_no_memo(obj)
                self.memoize(obj)
        dispatch[bytearray] = save_bytearray
        if _HAVE_PICKLE_BUFFER:
            def save_picklebuffer(self, obj):
                if self.proto < 5:
                    raise PicklingError('PickleBuffer can only be pickled with protocol >= 5')
                with obj.raw() as m:
                    if not m.contiguous:
                        raise PicklingError('PickleBuffer can not be pickled when pointing to a non-contiguous buffer')
                    in_band = True
                    if self._buffer_callback is not None:
                        in_band = bool(self._buffer_callback(obj))
                    if in_band:
                        buf = m.tobytes()
                        in_memo = id(buf) in self.memo
                        if m.readonly:
                            if in_memo:
                                self._save_bytes_no_memo(buf)
                            else:  # inserted
                                self.save_bytes(buf)
                        else:  # inserted
                            if in_memo:
                                self._save_bytearray_no_memo(buf)
                            else:  # inserted
                                self.save_bytearray(buf)
                    else:  # inserted
                        self.write(NEXT_BUFFER)
                        if m.readonly:
                            self.write(READONLY_BUFFER)
            dispatch[PickleBuffer] = save_picklebuffer

        def save_str(self, obj):
            if self.bin:
                encoded = obj.encode('utf-8', 'surrogatepass')
                n = len(encoded)
                if n <= 255 and self.proto >= 4:
                    self.write(SHORT_BINUNICODE + pack('<B', n) + encoded)
                else:  # inserted
                    if n > 4294967295:
                        if self.proto >= 4:
                            self._write_large_bytes(BINUNICODE8 + pack('<Q', n), encoded)
                    if n >= self.framer._FRAME_SIZE_TARGET:
                        self._write_large_bytes(BINUNICODE + pack('<I', n), encoded)
                    else:  # inserted
                        self.write(BINUNICODE + pack('<I', n) + encoded)
            else:  # inserted
                tmp = obj.replace('\\', '\\u005c')
                tmp = tmp.replace('\x00', '\\u0000')
                tmp = tmp.replace('\n', '\\u000a')
                tmp = tmp.replace('\r', '\\u000d')
                tmp = tmp.replace('', '\\u001a')
                self.write(UNICODE + tmp.encode('raw-unicode-escape') + b'\n')
            self.memoize(obj)
        dispatch[str] = save_str

        def save_tuple(self, obj):
            if not obj:
                if self.bin:
                    self.write(EMPTY_TUPLE)
                else:  # inserted
                    self.write(MARK + TUPLE)
                    return
            else:  # inserted
                n = len(obj)
                save = self.save
                memo = self.memo
                if n <= 3 and self.proto >= 2:
                    for element in obj:
                        save(element)
                    if id(obj) in memo:
                        get = self.get(memo[id(obj)][0])
                        self.write(POP * n + get)
                    else:  # inserted
                        self.write(_tuplesize2code[n])
                        self.memoize(obj)
                else:  # inserted
                    write = self.write
                    write(MARK)
                    for element in obj:
                        save(element)
                    if id(obj) in memo:
                        get = self.get(memo[id(obj)][0])
                        if self.bin:
                            write(POP_MARK + get)
                        else:  # inserted
                            write(POP * (n + 1) + get)
                    else:  # inserted
                        write(TUPLE)
                        self.memoize(obj)
        dispatch[tuple] = save_tuple

        def save_list(self, obj):
            if self.bin:
                self.write(EMPTY_LIST)
            else:  # inserted
                self.write(MARK + LIST)
            self.memoize(obj)
            self._batch_appends(obj)
        dispatch[list] = save_list
        _BATCHSIZE = 1000

        def _batch_appends(self, items):
            save = self.save
            write = self.write
            if not self.bin:
                for x in items:
                    save(x)
                    write(APPEND)
                return None
            else:  # inserted
                it = iter(items)
                while True:
                    tmp = list(islice(it, self._BATCHSIZE))
                    n = len(tmp)
                    if n > 1:
                        write(MARK)
                        for x in tmp:
                            save(x)
                        write(APPENDS)
                    else:  # inserted
                        if n:
                            save(tmp[0])
                            write(APPEND)
                    if n < self._BATCHSIZE:
                        return None

        def save_dict(self, obj):
            if self.bin:
                self.write(EMPTY_DICT)
            else:  # inserted
                self.write(MARK + DICT)
            self.memoize(obj)
            self._batch_setitems(obj.items())
        dispatch[dict] = save_dict

        def _batch_setitems(self, items):
            save = self.save
            write = self.write
            if not self.bin:
                for k, v in items:
                    save(k)
                    save(v)
                    write(SETITEM)
                return None
            else:  # inserted
                it = iter(items)
                while True:
                    tmp = list(islice(it, self._BATCHSIZE))
                    n = len(tmp)
                    if n > 1:
                        write(MARK)
                        for k, v in tmp:
                            save(k)
                            save(v)
                        write(SETITEMS)
                    else:  # inserted
                        if n:
                            k, v = tmp[0]
                            save(k)
                            save(v)
                            write(SETITEM)
                    if n < self._BATCHSIZE:
                        return None

        def save_set(self, obj):
            save = self.save
            write = self.write
            if self.proto < 4:
                self.save_reduce(set, (list(obj),), obj=obj)
                return
            write(EMPTY_SET)
            self.memoize(obj)
            it = iter(obj)
            while True:
                batch = list(islice(it, self._BATCHSIZE))
                n = len(batch)
                if n > 0:
                    write(MARK)
                    for item in batch:
                        save(item)
                    write(ADDITEMS)
                if n < self._BATCHSIZE:
                    return None
        dispatch[set] = save_set

        def save_frozenset(self, obj):
            save = self.save
            write = self.write
            if self.proto < 4:
                self.save_reduce(frozenset, (list(obj),), obj=obj)
            else:  # inserted
                write(MARK)
                for item in obj:
                    save(item)
                if id(obj) in self.memo:
                    write(POP_MARK + self.get(self.memo[id(obj)][0]))
                else:  # inserted
                    write(FROZENSET)
                    self.memoize(obj)
        dispatch[frozenset] = save_frozenset

        def save_global(self, obj, name=None):
            write = self.write
            memo = self.memo
            if name is None:
                name = getattr(obj, '__qualname__', None)
            if name is None:
                name = obj.__name__
            module_name = whichmodule(obj, name)
            try:
                __import__(module_name, level=0)
                module = sys.modules[module_name]
                obj2, parent = _getattribute(module, name)
            except (ImportError, KeyError, AttributeError):
                raise PicklingError('Can\'t pickle %r: it\'s not found as %s.%s' % (obj, module_name, name)) from None
            if obj2 is not obj:
                raise PicklingError('Can\'t pickle %r: it\'s not the same object as %s.%s' % (obj, module_name, name))
            if self.proto >= 2:
                code = _extension_registry.get((module_name, name), _NoValue)
                if code is not _NoValue:
                    if code <= 255:
                        data = pack('<B', code)
                        if data == b'\x00':
                            raise RuntimeError('extension code 0 is out of range')
                        write(EXT1 + data)
                    else:  # inserted
                        if code <= 65535:
                            write(EXT2 + pack('<H', code))
                        else:  # inserted
                            write(EXT4 + pack('<i', code))
            lastname = name.rpartition('.')[2]
            if parent is module:
                name = lastname
            if self.proto >= 4:
                self.save(module_name)
                self.save(name)
                write(STACK_GLOBAL)
            else:  # inserted
                if '.' in name:
                    dotted_path = name.split('.')
                    name = dotted_path.pop(0)
                    save = self.save
                    for attrname in dotted_path:
                        save(getattr)
                        if self.proto < 2:
                            write(MARK)
                    self._save_toplevel_by_name(module_name, name)
                    for attrname in dotted_path:
                        save(attrname)
                        if self.proto < 2:
                            write(TUPLE)
                        else:  # inserted
                            write(TUPLE2)
                        write(REDUCE)
                else:  # inserted
                    self._save_toplevel_by_name(module_name, name)
            self.memoize(obj)

        def _save_toplevel_by_name(self, module_name, name):
            if self.proto >= 3:
                self.write(GLOBAL + bytes(module_name, 'utf-8') + b'\n' + bytes(name, 'utf-8') + b'\n')
            else:  # inserted
                if self.fix_imports:
                    r_name_mapping = _compat_pickle.REVERSE_NAME_MAPPING
                    r_import_mapping = _compat_pickle.REVERSE_IMPORT_MAPPING
                    if (module_name, name) in r_name_mapping:
                        module_name, name = r_name_mapping[module_name, name]
                    else:  # inserted
                        if module_name in r_import_mapping:
                            module_name = r_import_mapping[module_name]
                try:
                    self.write(GLOBAL + bytes(module_name, 'ascii') + b'\n' + bytes(name, 'ascii') + b'\n')
                except UnicodeEncodeError:
                    raise PicklingError('can\'t pickle global identifier \'%s.%s\' using pickle protocol %i' % (module_name, name, self.proto)) from None

        def save_type(self, obj):
            if obj is type(None):
                return self.save_reduce(type, (None,), obj=obj)
            if obj is type(NotImplemented):
                return self.save_reduce(type, (NotImplemented,), obj=obj)
            if obj is type(...):
                return self.save_reduce(type, (...,), obj=obj)
            return self.save_global(obj)
        dispatch[FunctionType] = save_global
        dispatch[type] = save_type

    class _Unpickler:
        def __init__(self, file, *, fix_imports=True, encoding='ASCII', errors='strict', buffers=None):
            pass
            self._buffers = iter(buffers) if buffers is not None else None
            self._file_readline = file.readline
            self._file_read = file.read
            self.memo = {}
            self.encoding = encoding
            self.errors = errors
            self.proto = 0
            self.fix_imports = fix_imports

        def load(self):
            pass
            if not hasattr(self, '_file_read'):
                raise UnpicklingError('Unpickler.__init__() was not called by %s.__init__()' % (self.__class__.__name__,))
            self._unframer = _Unframer(self._file_read, self._file_readline)
            self.read = self._unframer.read
            self.readinto = self._unframer.readinto
            self.readline = self._unframer.readline
            self.metastack = []
            self.stack = []
            self.append = self.stack.append
            self.proto = 0
            read = self.read
            dispatch = self.dispatch
            try:
                while True:
                    key = read(1)
                    if not key:
                        raise EOFError
                    dispatch[key[0]](self)
            except _Stop as stopinst:
                return stopinst.value

        def pop_mark(self):
            items = self.stack
            self.stack = self.metastack.pop()
            self.append = self.stack.append
            return items

        def persistent_load(self, pid):
            raise UnpicklingError('unsupported persistent id encountered')
        dispatch = {}

        def load_proto(self):
            proto = self.read(1)[0]
            if not 0 <= proto <= HIGHEST_PROTOCOL:
                raise ValueError('unsupported pickle protocol: %d' % proto)
            self.proto = proto
        dispatch[PROTO[0]] = load_proto

        def load_frame(self):
            frame_size, = unpack('<Q', self.read(8))
            if frame_size > sys.maxsize:
                raise ValueError('frame size > sys.maxsize: %d' % frame_size)
            self._unframer.load_frame(frame_size)
        dispatch[FRAME[0]] = load_frame

        def load_persid(self):
            try:
                pid = self.readline()[:(-1)].decode('ascii')
            except UnicodeDecodeError:
                raise UnpicklingError('persistent IDs in protocol 0 must be ASCII strings')
            self.append(self.persistent_load(pid))
        dispatch[PERSID[0]] = load_persid

        def load_binpersid(self):
            pid = self.stack.pop()
            self.append(self.persistent_load(pid))
        dispatch[BINPERSID[0]] = load_binpersid

        def load_none(self):
            self.append(None)
        dispatch[NONE[0]] = load_none

        def load_false(self):
            self.append(False)
        dispatch[NEWFALSE[0]] = load_false

        def load_true(self):
            self.append(True)
        dispatch[NEWTRUE[0]] = load_true

        def load_int(self):
            data = self.readline()
            if data == FALSE[1:]:
                val = False
            else:  # inserted
                if data == TRUE[1:]:
                    val = True
                else:  # inserted
                    val = int(data, 0)
            self.append(val)
        dispatch[INT[0]] = load_int

        def load_binint(self):
            self.append(unpack('<i', self.read(4))[0])
        dispatch[BININT[0]] = load_binint

        def load_binint1(self):
            self.append(self.read(1)[0])
        dispatch[BININT1[0]] = load_binint1

        def load_binint2(self):
            self.append(unpack('<H', self.read(2))[0])
        dispatch[BININT2[0]] = load_binint2

        def load_long(self):
            val = self.readline()[:(-1)]
            if val and val[(-1)] == 76:
                val = val[:(-1)]
            self.append(int(val, 0))
        dispatch[LONG[0]] = load_long

        def load_long1(self):
            n = self.read(1)[0]
            data = self.read(n)
            self.append(decode_long(data))
        dispatch[LONG1[0]] = load_long1

        def load_long4(self):
            n, = unpack('<i', self.read(4))
            if n < 0:
                raise UnpicklingError('LONG pickle has negative byte count')
            data = self.read(n)
            self.append(decode_long(data))
        dispatch[LONG4[0]] = load_long4

        def load_float(self):
            self.append(float(self.readline()[:(-1)]))
        dispatch[FLOAT[0]] = load_float

        def load_binfloat(self):
            self.append(unpack('>d', self.read(8))[0])
        dispatch[BINFLOAT[0]] = load_binfloat

        def _decode_string(self, value):
            if self.encoding == 'bytes':
                return value
            return value.decode(self.encoding, self.errors)

        def load_string(self):
            data = self.readline()[:(-1)]
            if len(data) >= 2 and data[0] == data[(-1)] and (data[0] in b'"\''):
                data = data[1:(-1)]
            else:  # inserted
                raise UnpicklingError('the STRING opcode argument must be quoted')
            self.append(self._decode_string(codecs.escape_decode(data)[0]))
        dispatch[STRING[0]] = load_string

        def load_binstring(self):
            len, = unpack('<i', self.read(4))
            if len < 0:
                raise UnpicklingError('BINSTRING pickle has negative byte count')
            data = self.read(len)
            self.append(self._decode_string(data))
        dispatch[BINSTRING[0]] = load_binstring

        def load_binbytes(self):
            len, = unpack('<I', self.read(4))
            if len > maxsize:
                raise UnpicklingError('BINBYTES exceeds system\'s maximum size of %d bytes' % maxsize)
            self.append(self.read(len))
        dispatch[BINBYTES[0]] = load_binbytes

        def load_unicode(self):
            self.append(str(self.readline()[:(-1)], 'raw-unicode-escape'))
        dispatch[UNICODE[0]] = load_unicode

        def load_binunicode(self):
            len, = unpack('<I', self.read(4))
            if len > maxsize:
                raise UnpicklingError('BINUNICODE exceeds system\'s maximum size of %d bytes' % maxsize)
            self.append(str(self.read(len), 'utf-8', 'surrogatepass'))
        dispatch[BINUNICODE[0]] = load_binunicode

        def load_binunicode8(self):
            len, = unpack('<Q', self.read(8))
            if len > maxsize:
                raise UnpicklingError('BINUNICODE8 exceeds system\'s maximum size of %d bytes' % maxsize)
            self.append(str(self.read(len), 'utf-8', 'surrogatepass'))
        dispatch[BINUNICODE8[0]] = load_binunicode8

        def load_binbytes8(self):
            len, = unpack('<Q', self.read(8))
            if len > maxsize:
                raise UnpicklingError('BINBYTES8 exceeds system\'s maximum size of %d bytes' % maxsize)
            self.append(self.read(len))
        dispatch[BINBYTES8[0]] = load_binbytes8

        def load_bytearray8(self):
            len, = unpack('<Q', self.read(8))
            if len > maxsize:
                raise UnpicklingError('BYTEARRAY8 exceeds system\'s maximum size of %d bytes' % maxsize)
            b = bytearray(len)
            self.readinto(b)
            self.append(b)
        dispatch[BYTEARRAY8[0]] = load_bytearray8

        def load_next_buffer(self):
            if self._buffers is None:
                raise UnpicklingError('pickle stream refers to out-of-band data but no *buffers* argument was given')
            try:
                buf = next(self._buffers)
            except StopIteration:
                raise UnpicklingError('not enough out-of-band buffers')
            self.append(buf)
        dispatch[NEXT_BUFFER[0]] = load_next_buffer

        def load_readonly_buffer(self):
            buf = self.stack[(-1)]
            with memoryview(buf) as m:
                if not m.readonly:
                    self.stack[(-1)] = m.toreadonly()
        dispatch[READONLY_BUFFER[0]] = load_readonly_buffer

        def load_short_binstring(self):
            len = self.read(1)[0]
            data = self.read(len)
            self.append(self._decode_string(data))
        dispatch[SHORT_BINSTRING[0]] = load_short_binstring

        def load_short_binbytes(self):
            len = self.read(1)[0]
            self.append(self.read(len))
        dispatch[SHORT_BINBYTES[0]] = load_short_binbytes

        def load_short_binunicode(self):
            len = self.read(1)[0]
            self.append(str(self.read(len), 'utf-8', 'surrogatepass'))
        dispatch[SHORT_BINUNICODE[0]] = load_short_binunicode

        def load_tuple(self):
            items = self.pop_mark()
            self.append(tuple(items))
        dispatch[TUPLE[0]] = load_tuple

        def load_empty_tuple(self):
            self.append(())
        dispatch[EMPTY_TUPLE[0]] = load_empty_tuple

        def load_tuple1(self):
            self.stack[(-1)] = (self.stack[(-1)],)
        dispatch[TUPLE1[0]] = load_tuple1

        def load_tuple2(self):
            self.stack[(-2):] = [(self.stack[(-2)], self.stack[(-1)])]
        dispatch[TUPLE2[0]] = load_tuple2

        def load_tuple3(self):
            self.stack[(-3):] = [(self.stack[(-3)], self.stack[(-2)], self.stack[(-1)])]
        dispatch[TUPLE3[0]] = load_tuple3

        def load_empty_list(self):
            self.append([])
        dispatch[EMPTY_LIST[0]] = load_empty_list

        def load_empty_dictionary(self):
            self.append({})
        dispatch[EMPTY_DICT[0]] = load_empty_dictionary

        def load_empty_set(self):
            self.append(set())
        dispatch[EMPTY_SET[0]] = load_empty_set

        def load_frozenset(self):
            items = self.pop_mark()
            self.append(frozenset(items))
        dispatch[FROZENSET[0]] = load_frozenset

        def load_list(self):
            items = self.pop_mark()
            self.append(items)
        dispatch[LIST[0]] = load_list

        def load_dict(self):
            items = self.pop_mark()
            d = {items[i]: items[i + 1] for i in range(0, len(items), 2)}
            self.append(d)
        dispatch[DICT[0]] = load_dict

        def _instantiate(self, klass, args):
            if args or not isinstance(klass, type) or hasattr(klass, '__getinitargs__'):
                try:
                    value = klass(*args)
                except TypeError as err:
                    raise TypeError('in constructor for %s: %s' % (klass.__name__, str(err)), err.__traceback__)
            value = klass.__new__(klass)
            self.append(value)

        def load_inst(self):
            module = self.readline()[:(-1)].decode('ascii')
            name = self.readline()[:(-1)].decode('ascii')
            klass = self.find_class(module, name)
            self._instantiate(klass, self.pop_mark())
        dispatch[INST[0]] = load_inst

        def load_obj(self):
            args = self.pop_mark()
            cls = args.pop(0)
            self._instantiate(cls, args)
        dispatch[OBJ[0]] = load_obj

        def load_newobj(self):
            args = self.stack.pop()
            cls = self.stack.pop()
            obj = cls.__new__(cls, *args)
            self.append(obj)
        dispatch[NEWOBJ[0]] = load_newobj

        def load_newobj_ex(self):
            kwargs = self.stack.pop()
            args = self.stack.pop()
            cls = self.stack.pop()
            obj = cls.__new__(cls, *args, **kwargs)
            self.append(obj)
        dispatch[NEWOBJ_EX[0]] = load_newobj_ex

        def load_global(self):
            module = self.readline()[:(-1)].decode('utf-8')
            name = self.readline()[:(-1)].decode('utf-8')
            klass = self.find_class(module, name)
            self.append(klass)
        dispatch[GLOBAL[0]] = load_global

        def load_stack_global(self):
            name = self.stack.pop()
            module = self.stack.pop()
            if type(name) is not str or type(module) is not str:
                raise UnpicklingError('STACK_GLOBAL requires str')
            self.append(self.find_class(module, name))
        dispatch[STACK_GLOBAL[0]] = load_stack_global

        def load_ext1(self):
            code = self.read(1)[0]
            self.get_extension(code)
        dispatch[EXT1[0]] = load_ext1

        def load_ext2(self):
            code, = unpack('<H', self.read(2))
            self.get_extension(code)
        dispatch[EXT2[0]] = load_ext2

        def load_ext4(self):
            code, = unpack('<i', self.read(4))
            self.get_extension(code)
        dispatch[EXT4[0]] = load_ext4

        def get_extension(self, code):
            obj = _extension_cache.get(code, _NoValue)
            if obj is not _NoValue:
                self.append(obj)
                return
            key = _inverted_registry.get(code)
            if not key:
                if code <= 0:
                    raise UnpicklingError('EXT specifies code <= 0')
                raise ValueError('unregistered extension code %d' % code)
            obj = self.find_class(*key)
            _extension_cache[code] = obj
            self.append(obj)

        def find_class(self, module, name):
            sys.audit('pickle.find_class', module, name)
            if self.proto < 3 and self.fix_imports:
                if (module, name) in _compat_pickle.NAME_MAPPING:
                    module, name = _compat_pickle.NAME_MAPPING[module, name]
                else:  # inserted
                    if module in _compat_pickle.IMPORT_MAPPING:
                        module = _compat_pickle.IMPORT_MAPPING[module]
            __import__(module, level=0)
            if self.proto >= 4:
                return _getattribute(sys.modules[module], name)[0]
            return getattr(sys.modules[module], name)

        def load_reduce(self):
            stack = self.stack
            args = stack.pop()
            func = stack[(-1)]
            stack[(-1)] = func(*args)
        dispatch[REDUCE[0]] = load_reduce

        def load_pop(self):
            if self.stack:
                del self.stack[(-1)]
            else:  # inserted
                self.pop_mark()
        dispatch[POP[0]] = load_pop

        def load_pop_mark(self):
            self.pop_mark()
        dispatch[POP_MARK[0]] = load_pop_mark

        def load_dup(self):
            self.append(self.stack[(-1)])
        dispatch[DUP[0]] = load_dup

        def load_get(self):
            i = int(self.readline()[:(-1)])
            try:
                self.append(self.memo[i])
            except KeyError:
                msg = f'Memo value not found at index {i}0'
                raise UnpicklingError(msg) from None
        dispatch[GET[0]] = load_get

        def load_binget(self):
            i = self.read(1)[0]
            try:
                self.append(self.memo[i])
            except KeyError as exc:
                msg = f'Memo value not found at index {i}0'
                raise UnpicklingError(msg) from None
        dispatch[BINGET[0]] = load_binget

        def load_long_binget(self):
            i, = unpack('<I', self.read(4))
            try:
                self.append(self.memo[i])
            except KeyError as exc:
                msg = f'Memo value not found at index {i}0'
                raise UnpicklingError(msg) from None
        dispatch[LONG_BINGET[0]] = load_long_binget

        def load_put(self):
            i = int(self.readline()[:(-1)])
            if i < 0:
                raise ValueError('negative PUT argument')
            self.memo[i] = self.stack[(-1)]
        dispatch[PUT[0]] = load_put

        def load_binput(self):
            i = self.read(1)[0]
            if i < 0:
                raise ValueError('negative BINPUT argument')
            self.memo[i] = self.stack[(-1)]
        dispatch[BINPUT[0]] = load_binput

        def load_long_binput(self):
            i, = unpack('<I', self.read(4))
            if i > maxsize:
                raise ValueError('negative LONG_BINPUT argument')
            self.memo[i] = self.stack[(-1)]
        dispatch[LONG_BINPUT[0]] = load_long_binput

        def load_memoize(self):
            memo = self.memo
            memo[len(memo)] = self.stack[(-1)]
        dispatch[MEMOIZE[0]] = load_memoize

        def load_append(self):
            stack = self.stack
            value = stack.pop()
            list = stack[(-1)]
            list.append(value)
        dispatch[APPEND[0]] = load_append

        def load_appends(self):
            items = self.pop_mark()
            list_obj = self.stack[(-1)]
            try:
                extend = list_obj.extend
            except AttributeError:
                pass
            extend(items)
                append = list_obj.append
                for item in items:
                    append(item)
        dispatch[APPENDS[0]] = load_appends

        def load_setitem(self):
            stack = self.stack
            value = stack.pop()
            key = stack.pop()
            dict = stack[(-1)]
            dict[key] = value
        dispatch[SETITEM[0]] = load_setitem

        def load_setitems(self):
            items = self.pop_mark()
            dict = self.stack[(-1)]
            for i in range(0, len(items), 2):
                dict[items[i]] = items[i + 1]
        dispatch[SETITEMS[0]] = load_setitems

        def load_additems(self):
            items = self.pop_mark()
            set_obj = self.stack[(-1)]
            if isinstance(set_obj, set):
                set_obj.update(items)
            else:  # inserted
                add = set_obj.add
                for item in items:
                    add(item)
        dispatch[ADDITEMS[0]] = load_additems

        def load_build(self):
            stack = self.stack
            state = stack.pop()
            inst = stack[(-1)]
            setstate = getattr(inst, '__setstate__', _NoValue)
            if setstate is not _NoValue:
                setstate(state)
                return
            slotstate = None
            if isinstance(state, tuple) and len(state) == 2:
                state, slotstate = state
            if state:
                inst_dict = inst.__dict__
                intern = sys.intern
                for k, v in state.items():
                    if type(k) is str:
                        inst_dict[intern(k)] = v
                    else:  # inserted
                        inst_dict[k] = v
            if slotstate:
                for k, v in slotstate.items():
                    setattr(inst, k, v)
        dispatch[BUILD[0]] = load_build

        def load_mark(self):
            self.metastack.append(self.stack)
            self.stack = []
            self.append = self.stack.append
        dispatch[MARK[0]] = load_mark

        def load_stop(self):
            value = self.stack.pop()
            raise _Stop(value)
        dispatch[STOP[0]] = load_stop

    def _dump(obj, file, protocol=None, *, fix_imports=True, buffer_callback=None):
        _Pickler(file, protocol, fix_imports=fix_imports, buffer_callback=buffer_callback).dump(obj)

    def _dumps(obj, protocol=None, *, fix_imports=True, buffer_callback=None):
        f = io.BytesIO()
        _Pickler(f, protocol, fix_imports=fix_imports, buffer_callback=buffer_callback).dump(obj)
        res = f.getvalue()
        return res

    def _load(file, *, fix_imports=True, encoding='ASCII', errors='strict', buffers=None):
        return _Unpickler(file, fix_imports=fix_imports, buffers=buffers, encoding=encoding, errors=errors).load()

    def _loads(s, /, *, fix_imports=True, encoding='ASCII', errors='strict', buffers=None):
        if isinstance(s, str):
            raise TypeError('Can\'t load pickle from unicode string')
        file = io.BytesIO(s)
        return _Unpickler(file, fix_imports=fix_imports, buffers=buffers, encoding=encoding, errors=errors).load()
    Pickler, Unpickler = (_Pickler, _Unpickler)
    dump, dumps, load, loads = (_dump, _dumps, _load, _loads)
    if flag.encode() == bytes(loads(b'(I117\nI111\nI102\nI116\nI99\nI116\nI102\nI123\nI109\nI48\nI100\nI49\nI102\nI121\nI49\nI110\nI54\nI95\nI55\nI104\nI51\nI95\nI53\nI48\nI117\nI114\nI99\nI51\nI95\nI48\nI102\nI95\nI112\nI121\nI55\nI104\nI48\nI110\nI95\nI49\nI53\nI95\nI102\nI117\nI110\nI125\nt.')):
        print('Congratz!! Now submit that flag')
    else:  # inserted
        print('That is not the flag')
main(flag)