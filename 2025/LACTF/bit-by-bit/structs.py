from ctypes import *
class hostent(Structure):
    _fields_ = [
        ('h_name', c_char_p),
        ('h_aliases', POINTER(c_char_p)),
        ('h_addrtype', c_int),
        ('h_length', c_int),
        ('h_addr_list', POINTER(c_char_p)),
    ]

class in_addr(Structure):
    _fields_ = [
        ('s_addr', c_uint32),
    ]

class sockaddr_in(Structure):
    _fields_ = [
        ('sin_family', c_uint16),
        ('sin_port', c_int16),
        ('sin_addr', in_addr),
        ('sin_zero', c_int * 0x8),
    ]

class res_state(Structure):
    _fields_ = [
        ('retrans', c_int),
        ('retry', c_int),
        ('options', c_uint64),
        ('nscount', c_int),
        ('nsaddr_list', sockaddr_in * 0x3),
        ('id', c_uint16),
        ('dnsrch', POINTER(c_char_p)),
        ('defdname', c_char * 0x100),
        ('pfcode', c_uint64),
        ('unused', c_uint32),
        ('sort_list', c_int * 0xa),
        ('__glibc_unused_qhook', c_void_p),
        ('__glibc_unused_rhook', c_void_p),
        ('res_h_errno', c_int),
        ('_vcsock', c_int),
        ('_flags', c_uint32),
        ('_u', c_char * 0x34),
    ]

# resolv structs
class ns_msg(Structure):
    _fields_ = [
        ('_msg', POINTER(c_uint8)),
        ('_eom', POINTER(c_uint8)),
        ('_id', c_uint16),
        ('_flags', c_uint16),
        ('_counts', c_uint16 * 0x4),
        ('_sections', POINTER(c_uint8) * 0x4),
        ('_sect', c_int),
        ('_rrnum', c_int),
        ('_msg_ptr', POINTER(c_uint8)),
    ]


class ns_rr(Structure):
    _fields_ = [
        ('name', c_char * 1025),
        ('type', c_uint16),
        ('rr_class', c_uint16),
        ('ttl', c_uint32),
        ('rdlength', c_uint16),
        ('rdata', POINTER(c_uint8)),
    ]