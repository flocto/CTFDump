uint64_t should_drop_inner(int64_t* arg1)
{
    int64_t x0 = *(_ReadMSR(sp_el0) + 0x4d8);
    int64_t x19 = *arg1;
    int64_t x21 = arg1[1];
    void var_138;
    memcpy(&var_138, &data_400ad0, 0x100);
    uint64_t x0_3 = filp_open(x19, 0, 0);
    uint64_t x19_1 = x0_3;
    
    if (x0_3 == -0x1000 || x0_3 < -0x1000)
    {
        int64_t var_140 = 0;
        int64_t x0_4 = kernel_read();
        filp_close(x19_1, 0);
        
        if (x0_4 & 0xffffffff80000000)
            x19_1 = 0xfffffffb;
        else
            x19_1 = execute_filter(&var_138, 0x100, current_program, data_400de8);
    }
    
    complete(x21);
    
    if (x0 == *(_ReadMSR(sp_el0) + 0x4d8))
        return x19_1;
    
    __stack_chk_fail();
    /* no return */
}

int64_t spawn_filter_thread(int64_t arg1)
{
    int64_t x0 = *(_ReadMSR(sp_el0) + 0x4d8);
    int64_t s;
    __builtin_memset(&s, 0, 0x20);
    int64_t var_40;
    __init_swait_queue_head(&var_40, "&x->wait", &__key.0);
    int64_t var_58 = arg1;
    int64_t* var_50 = &s;
    int64_t result =
        kthread_create_on_node(should_drop_inner, &var_58, 0xffffffff, "should_drop_inner");
    
    if (result == -0x1000 || result < -0x1000)
    {
        wake_up_process();
        wait_for_completion(&s);
        result = kthread_stop(result);
    }
    
    if (x0 == *(_ReadMSR(sp_el0) + 0x4d8))
        return result;
    
    __stack_chk_fail();
    /* no return */
}

int64_t should_drop(int64_t arg1)
{
    int64_t x0 = *(_ReadMSR(sp_el0) + 0x4d8);
    void var_128;
    memset(&var_128, 0, 0x100);
    int64_t result;
    
    if (!current_program)
        result = -0x16;
    else if (strncpy_from_user(&var_128, arg1, 0x100) & 0xffffffff80000000)
        result = -0xe;
    else
        result = spawn_filter_thread(&var_128);
    
    if (x0 == *(_ReadMSR(sp_el0) + 0x4d8))
        return result;
    
    __stack_chk_fail();
    /* no return */
}

int64_t set_program(int64_t arg1)
{
    uint64_t x1 = _ReadMSR(sp_el0);
    uint64_t x2 = _ReadMSR(sp_el0);
    int32_t x3 = *(x2 + 0x2c);
    int64_t x4 = *(x1 + 0x4d8);
    int64_t var_38 = 0;
    int64_t var_30 = 0;
    int64_t x1_2;
    
    if (!(x3 & 0x200000))
        x1_2 = arg1;
    
    if (x3 & 0x200000 || *x2 & 0x4000000)
        x1_2 = arg1 & (arg1 & 0xffffffffffffff) << 8 >> 8;
    
    int64_t x0_1;
    
    if (x1_2 <= 0xffffffffffff0)
        x0_1 = __arch_copy_from_user(&var_38, arg1 & 0xff7fffffffffffff, 0x10);
    
    int64_t result;
    
    if (x1_2 > 0xffffffffffff0 || x0_1)
        result = -0xe;
    else if (var_30 > 0x1000)
        result = -0x16;
    else
    {
        int64_t x0_3 = __kmalloc_noprof(var_30, 0xcc0);
        
        if (!x0_3)
            result = -0xc;
        else
        {
            int64_t x1_4 = var_38;
            
            if (var_30 > 0x7fffffff)
                trap(0x800);
            
            uint64_t x2_1 = _ReadMSR(sp_el0);
            int64_t x0_4 = x1_4;
            
            if (*(x2_1 + 0x2c) & 0x200000 || *x2_1 & 0x4000000)
                x0_4 = x1_4 & (x1_4 & 0xffffffffffffff) << 8 >> 8;
            
            if (x0_4 <= 0x10000000000000 - var_30)
            {
                int64_t x0_9 = __arch_copy_from_user(x0_3, x1_4 & 0xff7fffffffffffff, var_30);
                
                if (!x0_9)
                {
                    label_400318:
                    int64_t current_program_1 = current_program;
                    
                    if (current_program_1)
                        kfree(current_program_1);
                    
                    current_program = x0_3;
                    data_400de8 = var_30;
                    result = 0;
                }
                else
                {
                    memset(x0_3 + var_30 - x0_9, 0, x0_9);
                    kfree(x0_3);
                    result = -0xe;
                }
            }
            else
            {
                memset(x0_3, 0, var_30);
                
                if (!var_30)
                    goto label_400318;
                
                kfree(x0_3);
                result = -0xe;
            }
        }
    }
    
    if (x4 == *(_ReadMSR(sp_el0) + 0x4d8))
        return result;
    
    int64_t x19;
    int64_t var_10_2 = x19;
    int64_t x20;
    int64_t var_8_2 = x20;
    __stack_chk_fail();
    /* no return */
}

int64_t device_ioctl(int64_t arg1, int32_t arg2, int64_t arg3)
{
    if (arg2 == 0x40086601)
        return set_program(arg3);
    
    if (arg2 != 0x40086602)
        return -0x16;
    
    return should_drop(arg3);
}

int64_t init_module()
{
    if (!proc_create("filter", 0x1b6, 0, &proc_ops))
        trap(0x800);
    
    return 0;
}

int64_t cleanup_module() __pure
{
    return;
}

int64_t eval_insn(int16_t* arg1, int64_t arg2)
{
    int32_t x3_27 = arg2 >> 8 & 0xf;
    uint16_t x6 = arg2 >> 0x10;
    uint32_t x5 = arg2 >> 0x10;
    uint16_t* x2;
    
    if (x3_27 == 4)
    {
        x2 = &arg1[5];
        label_4004e0:
        
        if (x2)
        {
            int32_t x3_1 = arg2 >> 0xc & 0xf;
            void* x4_1;
            
            if (x3_1 == 4)
            {
                x4_1 = &arg1[5];
                label_40051c:
                
                if (x4_1)
                    switch (arg2 & 0xff)
                    {
                        case 0:
                        {
                            return 0;
                            break;
                        }
                        case 1:
                        {
                            return 1;
                            break;
                        }
                        case 2:
                        {
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 3:
                        {
                            *arg1 = arg1[8];
                            return 2;
                            break;
                        }
                        case 4:
                        {
                            *x2 = *x4_1;
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 5:
                        {
                            *x2 = x6;
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 6:
                        {
                            *x2 += *x4_1;
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 7:
                        {
                            *x2 += x5;
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 8:
                        {
                            *x2 -= *x4_1;
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 9:
                        {
                            *x2 -= x5;
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 0xa:
                        {
                            *x2 *= *x4_1;
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 0xb:
                        {
                            *x2 *= x5;
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 0xc:
                        {
                            uint32_t x3_14 = *x4_1;
                            
                            if (x3_14)
                            {
                                *x2 = *x2 / x3_14;
                                *arg1 += 1;
                                return 2;
                            }
                            break;
                        }
                        case 0xd:
                        {
                            if (!x5)
                                trap(0x3e8);
                            
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 0xe:
                        {
                            *x2 = *x2 << *x4_1;
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 0xf:
                        {
                            *x2 = *x2 << x5;
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 0x10:
                        {
                            *x2 = *x2 >> *x4_1;
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 0x11:
                        {
                            *x2 = *x2 >> x5;
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 0x12:
                        {
                            *x2 &= *x4_1;
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 0x13:
                        {
                            *x2 &= x5;
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 0x14:
                        {
                            *x2 |= *x4_1;
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 0x15:
                        {
                            *x2 |= x5;
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 0x16:
                        {
                            arg1[9] = *x2 == *x4_1 ? 1 : 0;
                            *(arg1 + 0x13) = *x2 > *x4_1 ? 1 : 0;
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 0x17:
                        {
                            arg1[9] = *x2 == x5 ? 1 : 0;
                            *(arg1 + 0x13) = *x2 > x5 ? 1 : 0;
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 0x18:
                        {
                            *arg1 = *x2;
                            return 2;
                            break;
                        }
                        case 0x19:
                        {
                            *arg1 = x6;
                            return 2;
                            break;
                        }
                        case 0x1a:
                        {
                            arg1[8] = *arg1 + 1;
                            *arg1 = *x2;
                            return 2;
                            break;
                        }
                        case 0x1b:
                        {
                            int16_t x1_9 = *arg1;
                            *arg1 = x6;
                            arg1[8] = x1_9 + 1;
                            return 2;
                            break;
                        }
                        case 0x1c:
                        {
                            if (arg1[9] & 1)
                            {
                                *arg1 = *x2;
                                return 2;
                            }
                            
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 0x1d:
                        {
                            if (!(arg1[9] & 1))
                            {
                                *arg1 += 1;
                                return 2;
                            }
                            
                            *arg1 = x6;
                            return 2;
                            break;
                        }
                        case 0x1e:
                        {
                            if (!(arg1[9] & 1))
                            {
                                *arg1 = *x2;
                                return 2;
                            }
                            
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 0x1f:
                        {
                            if (!(arg1[9] & 1))
                            {
                                *arg1 = x6;
                                return 2;
                            }
                            
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 0x20:
                        {
                            if (*(arg1 + 0x13) & 1)
                            {
                                *arg1 = *x2;
                                return 2;
                            }
                            
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 0x21:
                        {
                            if (*(arg1 + 0x13) & 1)
                            {
                                *arg1 = x6;
                                return 2;
                            }
                            
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 0x22:
                        {
                            if (!(arg1[9] & 1) && !(*(arg1 + 0x13) & 1))
                            {
                                *arg1 = *x2;
                                return 2;
                            }
                            
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 0x23:
                        {
                            if (!(arg1[9] & 1) && !(*(arg1 + 0x13) & 1))
                            {
                                *arg1 = x6;
                                return 2;
                            }
                            
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 0x24:
                        {
                            if (*(arg1 + 0x10) & 0xffff0000)
                            {
                                *arg1 = *x2;
                                return 2;
                            }
                            
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 0x25:
                        {
                            if (*(arg1 + 0x10) & 0xffff0000)
                            {
                                *arg1 = x6;
                                return 2;
                            }
                            
                            *arg1 += 1;
                            return 2;
                            break;
                        }
                        case 0x26:
                        {
                            if (*(arg1 + 0x13) & 1 && !(arg1[9] & 1))
                            {
                                *arg1 += 1;
                                return 2;
                            }
                            
                            *arg1 = *x2;
                            return 2;
                            break;
                        }
                        case 0x27:
                        {
                            if (*(arg1 + 0x13) & 1 && !(arg1[9] & 1))
                            {
                                *arg1 += 1;
                                return 2;
                            }
                            
                            *arg1 = x6;
                            return 2;
                            break;
                        }
                        case 0x28:
                        {
                            uint32_t x1_67 = arg1[7];
                            
                            if (!((x1_67 <= 1 ? 1 : 0) | (x1_67 & 1)))
                            {
                                int64_t x3_18 = *(arg1 + 0x18);
                                uint32_t x1_69 = x1_67 - 2;
                                arg1[7] = x1_69;
                                *(x3_18 + x1_69) = *x2;
                                *arg1 += 1;
                                return 2;
                            }
                            break;
                        }
                        case 0x29:
                        {
                            uint32_t x1_70 = arg1[7];
                            
                            if (!(x1_70 & 1) && *(arg1 + 0x20) > x1_70)
                            {
                                *x2 = *(*(arg1 + 0x18) + x1_70);
                                arg1[7] += 2;
                                *arg1 += 1;
                                return 2;
                            }
                            break;
                        }
                        case 0x2a:
                        {
                            uint64_t x1_74 = *x4_1;
                            
                            if (x1_74 < *(arg1 + 0x20))
                            {
                                *x2 = *(*(arg1 + 0x18) + x1_74);
                                *arg1 += 1;
                                return 2;
                            }
                            break;
                        }
                        case 0x2b:
                        {
                            if (*(arg1 + 0x20) > x5)
                            {
                                *x2 = *(*(arg1 + 0x18) + x5);
                                *arg1 += 1;
                                return 2;
                            }
                            break;
                        }
                        case 0x2c:
                        {
                            uint64_t x1_79 = *x4_1;
                            
                            if (x1_79 < *(arg1 + 0x20))
                            {
                                *(*(arg1 + 0x18) + x1_79) = *x2;
                                *arg1 += 1;
                                return 2;
                            }
                            break;
                        }
                        case 0x2d:
                        {
                            if (*(arg1 + 0x20) > x5)
                            {
                                *(*(arg1 + 0x18) + x5) = *x2;
                                *arg1 += 1;
                                return 2;
                            }
                            break;
                        }
                        case 0x2e:
                        {
                            uint32_t x1_82 = *x4_1;
                            
                            if (!(x1_82 & 1) && *(arg1 + 0x20) > x1_82)
                            {
                                *x2 = *(*(arg1 + 0x18) + x1_82);
                                *arg1 += 1;
                                return 2;
                            }
                            break;
                        }
                        case 0x2f:
                        {
                            if (!(x5 & 1) && *(arg1 + 0x20) > x5)
                            {
                                *x2 = *(*(arg1 + 0x18) + x5);
                                *arg1 += 1;
                                return 2;
                            }
                            break;
                        }
                        case 0x30:
                        {
                            uint32_t x1_24 = *x4_1;
                            
                            if (!(x1_24 & 1) && *(arg1 + 0x20) > x1_24)
                            {
                                *(*(arg1 + 0x18) + x1_24) = *x2;
                                *arg1 += 1;
                                return 2;
                            }
                            break;
                        }
                        case 0x31:
                        {
                            if (!(x5 & 1) && *(arg1 + 0x20) > x5)
                            {
                                *(*(arg1 + 0x18) + x5) = *x2;
                                *arg1 += 1;
                                return 2;
                            }
                            break;
                        }
                    }
            }
            else
            {
                if (x3_1 <= 4)
                {
                    x4_1 = &arg1[3];
                    
                    if (x3_1 != 2)
                    {
                        x4_1 = &arg1[4];
                        
                        if (x3_1 != 3)
                        {
                            if (!x3_1)
                                x4_1 = &arg1[1];
                            else
                                x4_1 = &arg1[2];
                        }
                    }
                    
                    goto label_40051c;
                }
                
                if (x3_1 == 6)
                {
                    x4_1 = &arg1[7];
                    goto label_40051c;
                }
                
                if (x3_1 == 7)
                {
                    x4_1 = &arg1[8];
                    goto label_40051c;
                }
                
                x4_1 = &arg1[6];
                
                if (x3_1 == 5)
                    goto label_40051c;
            }
        }
    }
    else
    {
        if (x3_27 <= 4)
        {
            x2 = &arg1[3];
            
            if (x3_27 != 2)
            {
                x2 = &arg1[4];
                
                if (x3_27 != 3)
                {
                    if (!x3_27)
                        x2 = &arg1[1];
                    else
                        x2 = &arg1[2];
                }
            }
            
            goto label_4004e0;
        }
        
        if (x3_27 == 6)
        {
            x2 = &arg1[7];
            goto label_4004e0;
        }
        
        if (x3_27 == 7)
        {
            x2 = &arg1[8];
            goto label_4004e0;
        }
        
        x2 = &arg1[6];
        
        if (x3_27 == 5)
            goto label_4004e0;
    }
    return 0xffffffff;
}

int64_t execute_filter(int64_t arg1, int64_t arg2, int64_t arg3, int64_t arg4)
{
    int64_t x2 = *(_ReadMSR(sp_el0) + 0x4d8);
    uint32_t x2_1 = 0;
    int64_t s;
    __builtin_memset(&s, 0, 0x18);
    int64_t var_38;
    *var_38[6] = arg2;
    int64_t var_28 = arg1;
    int64_t var_20 = arg2;
    int64_t result;
    
    while (true)
    {
        uint64_t x0 = x2_1;
        
        if (x0 < arg4 >> 2)
        {
            s = x2_1;
            int32_t x0_2 = eval_insn(&s, *(arg3 + (x0 << 2)));
            
            if (!x0_2)
            {
                result = 0;
                break;
            }
            
            if (x0_2 == 1)
            {
                result = 1;
                break;
            }
            
            if (x0_2 != 0xffffffff)
            {
                x2_1 = s;
                continue;
            }
        }
        
        result = -0x16;
        break;
    }
    
    if (x2 == *(_ReadMSR(sp_el0) + 0x4d8))
        return result;
    
    __stack_chk_fail();
    /* no return */
}

void sub_400aa0() __noreturn
{
    trap(0);
}

