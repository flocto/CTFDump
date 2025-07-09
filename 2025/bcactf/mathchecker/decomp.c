void _start() __noreturn
{
    syscall(3, 0, &buf, 0xa);
    int32_t eax_2 = ((*(buf + 1)) - 0x30) * 5;
    
    if (eax_2 == 0x28)
    {
        int32_t eax_7 = ((*(buf + 2)) - 0x30) * 0x10 + 2;
        int32_t edx_1 = 0;
        
        if (COMBINE(edx_1, eax_7) / 0x1a == 5 && !(COMBINE(edx_1, eax_7) % 0x1a) && *buf == 0x31)
        {
            int32_t eax_16 = eax_2 + ((*(buf + 3)) - 0x30) * 0xa + data_804a004 - 0x30;
            int32_t edx_3 = 0;
            
            if (COMBINE(edx_3, eax_16) / 0x13 == 7 && !(COMBINE(edx_3, eax_16) % 0x13))
            {
                int32_t eax_20 = (data_804a006 - 0x30) * 5;
                
                if (eax_20 == 0x28)
                {
                    int32_t eax_25 = (data_804a007 - 0x30) * 0x10 + 2;
                    int32_t edx_5 = 0;
                    
                    if (COMBINE(edx_5, eax_25) / 0x1a == 5 && !(COMBINE(edx_5, eax_25) % 0x1a)
                        && data_804a005 == 0x32)
                    {
                        int32_t eax_34 = eax_20 + (data_804a008 - 0x30) * 0xa + data_804a009 - 0x30;
                        int32_t edx_7 = 0;
                        
                        if (COMBINE(edx_7, eax_34) / 0x13 == 7 && !(COMBINE(edx_7, eax_34) % 0x13))
                            /* tailcall */
                            return end();
                    }
                }
            }
        }
    }
    
    syscall(4, 1, &fail_msg, 1);
    print_newline();
    syscall(sys_exit {1}, 1);
    /* no return */
}

int32_t print_newline()
{
    buf = 0xa;
    return syscall(4, 1, &buf, 1);
}

void end() __noreturn
{
    syscall(4, 1, &good_msg, 2);
    print_newline();
    syscall(sys_exit {1}, 0);
    /* no return */
}

