function check(input) {
    var f,
        buf,
        e,
        n,
        i,
        u,
        a,
        t,
        b,
        c,
        k,
        p,
        h,
        s,
        l,
        d,
        W,
        g,
        x,
        G,
        V,
        _,
        w,
        m,
        y,
        j,
        C = 62802, // 1111010101010010
        callstack = [],
        stack = [];
    r: for (;;) {
        f: for (;;) {
            
            if (!(1 & C)) {
                break f;
            }
            o: for (;;) {
                if (!(1024 & C)) {
                    break o;
                }
                e: for (;;) {
                    if (!(128 & C)) {
                        break e;
                    }
                    n: for (;;) {
                        if (!(4 & C)) {
                            break n;
                        }
                        i: for (;;) {
                            if (!(8 & C)) {
                                break i;
                            }
                            u: for (;;) {
                                if (!(64 & C)) {
                                    break u;
                                }
                                a: for (;;) {
                                    if (!(4096 & C)) {
                                        break a;
                                    }
                                    t: for (;;) {
                                        if (!(32 & C)) {
                                            break t;
                                        }
                                        (_ = stack[stack.length - 1]), (C = 5572);
                                        continue a;
                                    }
                                    for (;;) {
                                        (w = Object.keys(_).reduce(
                                            (r, f) => (
                                                (r[f.charCodeAt(0)] =
                                                    _[f].length),
                                                r
                                            ),
                                            []
                                        )),
                                            (C = 45381);
                                        continue f;
                                    }
                                }
                                for (;;) {
                                    a: for (;;) {
                                        if (!(512 & C)) {
                                            break a;
                                        }
                                        stack.push(V + 1), (C = 46908);
                                        continue r;
                                    }
                                    for (;;) {
                                        stack.pop(), (C = 38094);
                                        continue r;
                                    }
                                }
                            }
                            for (;;) {
                                u: for (;;) {
                                    if (!(4096 & C)) {
                                        break u;
                                    }
                                    a: for (;;) {
                                        if (!(8192 & C)) {
                                            break a;
                                        }
                                        (f[G.c] = stack[stack.length - 2]), (C = 37754);
                                        continue r;
                                    }
                                    a: for (
                                        ;
                                        16176 !=
                                        (C = 38016 * (null === G.c) + 16176);

                                    )
                                        continue r;
                                }
                                for (;;) {
                                    u: for (;;) {
                                        if (!(2 & C)) {
                                            break u;
                                        }
                                        (V = stack[stack.length - 2]), (C = 58088);
                                        continue i;
                                    }
                                    for (;;) {
                                        callstack.push(32972), (C = 33799);
                                        continue n;
                                    }
                                }
                            }
                        }
                        for (;;) {
                            i: for (;;) {
                                if (!(2048 & C)) {
                                    break i;
                                }
                                u: for (;;) {
                                    if (!(2 & C)) {
                                        break u;
                                    }
                                    a: for (;;) {
                                        if (!(8192 & C)) {
                                            break a;
                                        }
                                        C = 4206;
                                        continue r;
                                    }
                                    a: for (;;) {
                                        stack.pop(), (C = 45022);
                                        break a;
                                    }
                                }
                                for (;;) {
                                    u: for (;;) {
                                        if (!(64 & C)) {
                                            break u;
                                        }
                                        C = 38962;
                                        continue r;
                                    }
                                    u: for (
                                        ;
                                        55380 != (C = -17174 * !!G + 55380);

                                    )
                                        continue n;
                                }
                            }
                            i: for (;;) {
                                u: for (;;) {
                                    if (!(512 & C)) {
                                        break u;
                                    }
                                    a: for (;;) {
                                        if (!(64 & C)) {
                                            break a;
                                        }
                                        stack.pop(), (C = 8404);
                                        continue i;
                                    }
                                    for (;;) {
                                        W++, (C = 32576);
                                        continue r;
                                    }
                                }
                                for (;;) {
                                    u: for (;;) {
                                        if (!(32768 & C)) {
                                            break u;
                                        }
                                        (G = stack[stack.length - 1]), (C = 63424);
                                        continue r;
                                    }
                                    for (;;) {
                                        stack.push(d), (C = 44876);
                                        continue r;
                                    }
                                }
                            }
                        }
                    }
                    n: for (;;) {
                        i: for (;;) {
                            if (!(64 & C)) {
                                break i;
                            }
                            u: for (;;) {
                                if (!(32768 & C)) {
                                    break u;
                                }
                                a: for (;;) {
                                    if (!(4096 & C)) {
                                        break a;
                                    }
                                    t: for (;;) {
                                        if (!(8 & C)) {
                                            break t;
                                        }
                                        (W <<= l[x][1] - g), (C = 41708);
                                        continue u;
                                    }
                                    t: for (
                                        ;
                                        40620 !=
                                        (C = 698 * (l[x][1] === g) + 40620);

                                    )
                                        continue u;
                                }
                                a: for (;;) {
                                    t: for (;;) {
                                        if (!(512 & C)) {
                                            break t;
                                        }
                                        (g = l[x][1]), (C = 42183);
                                        continue a;
                                    }
                                    for (;;) {
                                        (d[l[x][0]] = W.toString(2).padStart(
                                            l[x][1],
                                            "0"
                                        )),
                                            (C = 42917);
                                        continue e;
                                    }
                                }
                            }
                            u: for (;;) {
                                a: for (;;) {
                                    if (!(512 & C)) {
                                        break a;
                                    }
                                    t: for (;;) {
                                        if (!(8192 & C)) {
                                            break t;
                                        }
                                        (d = {}), (C = 5719);
                                        continue a;
                                    }
                                    for (;;) {
                                        (W = 0), (C = 23560);
                                        continue u;
                                    }
                                }
                                for (;;) {
                                    a: for (;;) {
                                        if (!(32 & C)) {
                                            break a;
                                        }
                                        (x = 0), (C = 10076);
                                        continue r;
                                    }
                                    a: for (;;) {
                                        (g = 0), (C = 55465);
                                        break a;
                                    }
                                }
                            }
                        }
                        i: for (;;) {
                            u: for (;;) {
                                if (!(4096 & C)) {
                                    break u;
                                }
                                a: for (;;) {
                                    if (!(16 & C)) {
                                        break a;
                                    }
                                    t: for (;;) {
                                        if (!(8192 & C)) {
                                            break t;
                                        }
                                        callstack.push(38033), (C = 62612);
                                        continue e;
                                    }
                                    for (;;) {
                                        (l = Object.entries(f).sort(
                                            (r, f) =>
                                                r[1] - f[1] ||
                                                r[0].localeCompare(f[0])
                                        )),
                                            (C = 27489);
                                        continue n;
                                    }
                                }
                                for (;;) {
                                    a: for (;;) {
                                        if (!(32768 & C)) {
                                            break a;
                                        }
                                        stack.push(s), (C = 48921);
                                        continue u;
                                    }
                                    a: for (;;) {
                                        stack.push(0), (C = 45249);
                                        break a;
                                    }
                                }
                            }
                            for (;;) {
                                u: for (;;) {
                                    if (!(8 & C)) {
                                        break u;
                                    }
                                    a: for (;;) {
                                        if (!(16384 & C)) {
                                            break a;
                                        }
                                        c.sort((r, f) => r.f - f.f),
                                            (C = 46236);
                                        continue u;
                                    }
                                    for (;;) {
                                        C = 2466;
                                        continue r;
                                    }
                                }
                                u: for (;;) {
                                    a: for (;;) {
                                        if (!(16 & C)) {
                                            break a;
                                        }
                                        (s = c[0]), (C = 4933);
                                        continue u;
                                    }
                                    for (;;) {
                                        (f = {}), (C = 7944);
                                        continue i;
                                    }
                                }
                            }
                        }
                    }
                }
                e: for (;;) {
                    n: for (;;) {
                        if (!(8 & C)) {
                            break n;
                        }
                        i: for (;;) {
                            if (!(2048 & C)) {
                                break i;
                            }
                            u: for (;;) {
                                if (!(4 & C)) {
                                    break u;
                                }
                                a: for (;;) {
                                    if (!(8192 & C)) {
                                        break a;
                                    }
                                    t: for (;;) {
                                        if (!(2 & C)) {
                                            break t;
                                        }
                                        stack.push("dW1xKnVFWH5"), (C = 51538);
                                        continue r;
                                    }
                                    t: for (;;) {
                                        stack.push(387656501), (C = 46311);
                                        break t;
                                    }
                                }
                                for (;;) {
                                    a: for (;;) {
                                        if (!(64 & C)) {
                                            break a;
                                        }
                                        stack.push("dW1xLHXNcGp"), (C = 31812);
                                        continue u;
                                    }
                                    for (;;) {
                                        stack.push(236723758), (C = 14743);
                                        continue f;
                                    }
                                }
                            }
                            for (;;) {
                                u: for (;;) {
                                    if (!(32 & C)) {
                                        break u;
                                    }
                                    a: for (;;) {
                                        if (!(16 & C)) {
                                            break a;
                                        }
                                        callstack.push(39957), (C = 44352);
                                        continue e;
                                    }
                                    for (;;) {
                                        if (
                                            21079 ==
                                            (C =
                                                10010 *
                                                    (null === stack[stack.length - 1]) +
                                                21079)
                                        )
                                            continue f;
                                        continue f;
                                    }
                                }
                                u: for (;;) {
                                    a: for (;;) {
                                        if (!(2 & C)) {
                                            break a;
                                        }
                                        stack.push("dW1xKnVFcS9"), (C = 61196);
                                        continue u;
                                    }
                                    for (;;) {
                                        stack.push(303307048), (C = 29171);
                                        continue f;
                                    }
                                }
                            }
                        }
                        i: for (;;) {
                            u: for (;;) {
                                if (!(4096 & C)) {
                                    break u;
                                }
                                a: for (;;) {
                                    if (!(4 & C)) {
                                        break a;
                                    }
                                    t: for (;;) {
                                        if (!(32 & C)) {
                                            break t;
                                        }
                                        stack.push(185603370), (C = 21674);
                                        continue r;
                                    }
                                    t: for (;;) {
                                        stack.push("dW1xL3VucGp"), (C = 23141);
                                        break t;
                                    }
                                }
                                for (;;) {
                                    a: for (;;) {
                                        if (!(32768 & C)) {
                                            break a;
                                        }
                                        stack.push("dW1xKtVtdmp"), (C = 60081);
                                        continue f;
                                    }
                                    for (;;) {
                                        stack.push(168895531), (C = 21901);
                                        continue u;
                                    }
                                }
                            }
                            u: for (;;) {
                                a: for (;;) {
                                    if (!(32 & C)) {
                                        break a;
                                    }
                                    t: for (;;) {
                                        if (!(32768 & C)) {
                                            break t;
                                        }
                                        stack.push("dW1xKPZtcGp"), (C = 13481);
                                        continue a;
                                    }
                                    for (;;) {
                                        stack.push(135141663), (C = 34001);
                                        continue u;
                                    }
                                }
                                a: for (;;) {
                                    t: for (;;) {
                                        if (!(2 & C)) {
                                            break t;
                                        }
                                        stack.push(152903206), (C = 45643);
                                        continue i;
                                    }
                                    for (;;) {
                                        stack.push("dW1xKiVtdmp"), (C = 17551);
                                        continue a;
                                    }
                                }
                            }
                        }
                    }
                    for (;;) {
                        n: for (;;) {
                            if (!(32768 & C)) {
                                break n;
                            }
                            i: for (;;) {
                                if (!(16384 & C)) {
                                    break i;
                                }
                                u: for (;;) {
                                    if (!(2 & C)) {
                                        break u;
                                    }
                                    a: for (;;) {
                                        if (!(2048 & C)) {
                                            break a;
                                        }
                                        (stack[stack.length - 1] = ""), (C = 5522);
                                        continue u;
                                    }
                                    for (;;) {
                                        (t = {}), (C = 57220);
                                        continue i;
                                    }
                                }
                                u: for (;;) {
                                    a: for (;;) {
                                        if (!(256 & C)) {
                                            break a;
                                        }
                                        (b = 0), (C = 41653);
                                        continue u;
                                    }
                                    for (;;) {
                                        if (
                                            26645 ==
                                            (C =
                                                -24747 * (b >= a.length) +
                                                26645)
                                        )
                                            continue f;
                                        continue r;
                                    }
                                }
                            }
                            i: for (;;) {
                                u: for (;;) {
                                    if (!(256 & C)) {
                                        break u;
                                    }
                                    a: for (;;) {
                                        if (!(512 & C)) {
                                            break a;
                                        }
                                        return !1;
                                    }
                                    for (;;) {
                                        (a = stack[stack.length - 1]), (C = 60302);
                                        continue n;
                                    }
                                }
                                for (;;) {
                                    u: for (;;) {
                                        if (!(2048 & C)) {
                                            break u;
                                        }
                                        callstack.push(37941), (C = 8188);
                                        continue o;
                                    }
                                    for (;;) {
                                        let tos = stack[stack.length - 1];
                                        tos = tos.substring(i.length, i.length + stack[stack.length - 2].length);
                                        console.log(tos);
                                        console.log(stack[stack.length - 2]);
                                        if (
                                            54350 ==
                                            (C =
                                                -47416 *
                                                    !stack.pop().startsWith(
                                                        i + stack.pop() + u
                                                    ) +
                                                54350)
                                        ) // bp here part 2 to check TOS condition
                                            continue r;
                                        continue i;
                                    }
                                }
                            }
                        }
                        n: for (;;) {
                            i: for (;;) {
                                if (!(2 & C)) {
                                    break i;
                                }
                                u: for (;;) {
                                    if (!(32 & C)) {
                                        break u;
                                    }
                                    a: for (;;) {
                                        if (!(512 & C)) {
                                            break a;
                                        }
                                        (k = c.shift()), (C = 14377);
                                        continue u;
                                    }
                                    for (;;) {
                                        (p = c.shift()), (C = 3280);
                                        continue n;
                                    }
                                }
                                u: for (;;) {
                                    a: for (;;) {
                                        if (!(16 & C)) {
                                            break a;
                                        }
                                        (c = Object.entries(t).map(
                                            ([r, f]) => ({
                                                c: r,
                                                f: f,
                                                x: null,
                                                y: null,
                                            })
                                        )),
                                            (C = 36424);
                                        continue u;
                                    }
                                    for (;;) {
                                        c.sort((r, f) => r.f - f.f),
                                            (C = 38112);
                                        continue r;
                                    }
                                }
                            }
                            i: for (;;) {
                                u: for (;;) {
                                    if (!(4096 & C)) {
                                        break u;
                                    }
                                    a: for (;;) {
                                        if (!(256 & C)) {
                                            break a;
                                        }
                                        (h.y = p), (C = 38622);
                                        continue u;
                                    }
                                    for (;;) {
                                        c.push(h), (C = 28073);
                                        continue o;
                                    }
                                }
                                u: for (;;) {
                                    a: for (;;) {
                                        if (!(16 & C)) {
                                            break a;
                                        }
                                        (h = {
                                            c: null,
                                            f: k.f + p.f,
                                            x: null,
                                            y: null,
                                        }),
                                            (C = 47);
                                        continue u;
                                    }
                                    for (;;) {
                                        (h.x = k), (C = 7452);
                                        continue i;
                                    }
                                }
                            }
                        }
                    }
                }
            }
            for (;;) {
                o: for (;;) {
                    if (!(16 & C)) {
                        break o;
                    }
                    e: for (;;) {
                        if (!(8 & C)) {
                            break e;
                        }
                        n: for (;;) {
                            if (!(32768 & C)) {
                                break n;
                            }
                            i: for (;;) {
                                if (!(4096 & C)) {
                                    break i;
                                }
                                u: for (;;) {
                                    if (!(8192 & C)) {
                                        break u;
                                    }
                                    a: for (;;) {
                                        if (!(4 & C)) {
                                            break a;
                                        }
                                        stack.pop(), (C = 31811);
                                        continue u;
                                    }
                                    for (;;) {
                                        stack.push(j), (C = 8764);
                                        continue r;
                                    }
                                }
                                for (;;) {
                                    (u =
                                        btoa("pjumpjumpjumpjumpj").substring(
                                            3
                                        )),
                                        (C = 25858);
                                    continue r;
                                }
                            }
                            for (;;) {
                                i: for (;;) {
                                    if (!(64 & C)) {
                                        break i;
                                    }
                                    u: for (;;) {
                                        if (!(16384 & C)) {
                                            break u;
                                        }
                                        (y = stack[stack.length - 1]), (C = 38354);
                                        continue i;
                                    }
                                    for (;;) {
                                        (j = ""), (C = 59740);
                                        continue r;
                                    }
                                }
                                for (;;) {
                                    i: for (;;) {
                                        if (!(2048 & C)) {
                                            break i;
                                        }
                                        (j += input[(y >> 24) & 255]), (C = 45774);
                                        continue n;
                                    }
                                    i: for (;;) {
                                        (j += input[(y >> 16) & 255]), (C = 12081);
                                        break i;
                                    }
                                }
                            }
                        }
                        for (;;) {
                            n: for (;;) {
                                if (!(128 & C)) {
                                    break n;
                                }
                                i: for (;;) {
                                    if (!(16384 & C)) {
                                        break i;
                                    }
                                    stack.push(253767992), (C = 11724);
                                    continue r;
                                }
                                for (;;) {
                                    stack.push("dW1wCnVt1Wp"), (C = 41118);
                                    continue r;
                                }
                            }
                            n: for (;;) {
                                i: for (;;) {
                                    if (!(256 & C)) {
                                        break i;
                                    }
                                    stack.push("dW1wQnBtaGp"), (C = 13896);
                                    continue n;
                                }
                                for (;;) {
                                    stack.push(51782960), (C = 63666);
                                    continue r;
                                }
                            }
                        }
                    }
                    for (;;) {
                        e: for (;;) {
                            if (!(128 & C)) {
                                break e;
                            }
                            n: for (;;) {
                                if (!(4096 & C)) {
                                    break n;
                                }
                                i: for (;;) {
                                    if (!(32 & C)) {
                                        break i;
                                    }
                                    stack.push("dW1wQtXNWGp"), (C = 17480);
                                    continue r;
                                }
                                for (;;) {
                                    stack.push("dW1wCnVFcG9"), (C = 18692);
                                    continue r;
                                }
                            }
                            n: for (;;) {
                                i: for (;;) {
                                    if (!(32 & C)) {
                                        break i;
                                    }
                                    stack.push(153103667), (C = 43227);
                                    continue n;
                                }
                                for (;;) {
                                    stack.push("dW1xKn9ucGp"), (C = 22025);
                                    continue f;
                                }
                            }
                        }
                        for (;;) {
                            e: for (;;) {
                                if (!(4096 & C)) {
                                    break e;
                                }
                                n: for (;;) {
                                    if (!(32 & C)) {
                                        break n;
                                    }
                                    return !0;
                                }
                                for (;;) { // STARTRS HERE REAL
                                    callstack.push(60537), (C = 50040);
                                    continue o;
                                }
                            }
                            e: for (;;) {
                                n: for (;;) {
                                    if (!(16384 & C)) {
                                        break n;
                                    }
                                    (t[a[b]] = (t[a[b]] || 0) + 1), (C = 35662);
                                    continue e;
                                }
                                for (;;) {
                                    b++, (C = 39088);
                                    continue r;
                                }
                            }
                        }
                    }
                }
                o: for (;;) {
                    e: for (;;) {
                        if (!(8192 & C)) {
                            break e;
                        }
                        n: for (;;) {
                            if (!(32768 & C)) {
                                break n;
                            }
                            i: for (;;) {
                                if (!(4 & C)) {
                                    break i;
                                }
                                u: for (;;) {
                                    if (!(64 & C)) {
                                        break u;
                                    }
                                    a: for (;;) {
                                        if (!(2048 & C)) {
                                            break a;
                                        }
                                        (e = 0), (C = 54534);
                                        continue i;
                                    }
                                    a: for (;;) {
                                        (buf = []), (C = 31841);
                                        break a;
                                    }
                                }
                                u: for (;;) {
                                    a: for (;;) {
                                        if (!(256 & C)) {
                                            break a;
                                        }
                                        (n = 0), (C = 24080);
                                        continue u;
                                    }
                                    for (;;) {
                                        (m = 0), (C = 42467);
                                        continue n;
                                    }
                                }
                            }
                            i: for (;;) {
                                u: for (;;) {
                                    if (!(32 & C)) {
                                        break u;
                                    }
                                    a: for (;;) {
                                        if (!(64 & C)) {
                                            break a;
                                        }
                                        if (
                                            1572 ==
                                            (C = 51682 * (m >= 256) + 1572)
                                        )
                                            continue u;
                                        continue o; // breakpoint here and look at o
                                    }
                                    for (;;) {
                                        if (
                                            56088 ==
                                            (C =
                                                -23252 * ((w[m] || 0) <= 0) +
                                                56088)
                                        )
                                            continue i;
                                        continue o;
                                    }
                                }
                                for (;;) {
                                    u: for (;;) {
                                        if (!(2 & C)) {
                                            break u;
                                        }
                                        callstack.push(29445), (C = 35621);
                                        continue o;
                                    }
                                    u: for (;;) {
                                        stack.push(1), (C = 14226);
                                        break u;
                                    }
                                }
                            }
                        }
                        for (;;) {
                            n: for (;;) {
                                if (!(2 & C)) {
                                    break n;
                                }
                                i: for (;;) {
                                    if (!(4 & C)) {
                                        break i;
                                    }
                                    u: for (;;) {
                                        if (!(4096 & C)) {
                                            break u;
                                        }
                                        callstack.push(27215), (C = 35876);
                                        continue o;
                                    }
                                    for (;;) {
                                        stack.push(1 & (w[m] >>= 1)), (C = 771);
                                        continue n;
                                    }
                                }
                                for (;;) {
                                    i: for (;;) {
                                        if (!(64 & C)) {
                                            break i;
                                        }
                                        callstack.push(705), (C = 40704);
                                        continue o;
                                    }
                                    for (;;) {
                                        callstack.push(29984), (C = 22784);
                                        continue o;
                                    }
                                }
                            }
                            n: for (;;) {
                                i: for (;;) {
                                    if (!(32 & C)) {
                                        break i;
                                    }
                                    u: for (;;) {
                                        if (!(2048 & C)) {
                                            break u;
                                        }
                                        stack.push(1 & (w[m] >>= 1)), (C = 34218);
                                        continue i;
                                    }
                                    for (;;) {
                                        callstack.push(59132), (C = 3616);
                                        continue o;
                                    }
                                }
                                i: for (;;) {
                                    u: for (;;) {
                                        if (!(4 & C)) {
                                            break u;
                                        }
                                        (w[m] <<= 1), (C = 11073);
                                        continue i;
                                    }
                                    for (;;) {
                                        C = 51953;
                                        continue n;
                                    }
                                }
                            }
                        }
                    }
                    e: for (;;) {
                        n: for (;;) {
                            if (!(2048 & C)) {
                                break n;
                            }
                            i: for (;;) {
                                if (!(8 & C)) {
                                    break i;
                                }
                                u: for (;;) {
                                    if (!(64 & C)) {
                                        break u;
                                    }
                                    a: for (;;) {
                                        if (!(4 & C)) {
                                            break a;
                                        }
                                        (n = 0), (C = 50717);
                                        continue i;
                                    }
                                    a: for (;;) {
                                        (e = 0), (C = 14031);
                                        break a;
                                    }
                                }
                                for (;;) {
                                    u: for (;;) {
                                        if (!(256 & C)) {
                                            break u;
                                        }
                                        C = callstack.pop();
                                        continue r;
                                    }
                                    u: for (;;) {
                                        stack.pop(), (C = 4893);
                                        break u;
                                    }
                                }
                            }
                            i: for (;;) {
                                u: for (;;) {
                                    if (!(128 & C)) {
                                        break u;
                                    }
                                    a: for (;;) {
                                        if (!(32768 & C)) {
                                            break a;
                                        }
                                        if (e) {
                                            console.log('non-zero', e);
                                        }
                                        buf.push(
                                            e ^ "jump".charCodeAt(buf.length % 4)
                                        ),
                                            (C = 43130);
                                        continue n;
                                    }
                                    a: for (
                                        ;
                                        65231 !=
                                        (C = -37553 * (8 !== n) + 65231);

                                    )
                                        continue n;
                                }
                                for (;;) {
                                    u: for (;;) {
                                        if (!(2 & C)) {
                                            break u;
                                        }
                                        n++, (C = 27813);
                                        continue i;
                                    }
                                    u: for (;;) {
                                        // DEBUG
                                        if (stack[stack.length - 1]) {
                                            console.log(e, buf.length, n, m, String.fromCharCode(m), stack[stack.length - 1]);
                                        }
                                        (e = (e << 1) | stack[stack.length - 1]),
                                            (C = 52251);
                                        break u;
                                    }
                                }
                            }
                        }
                        for (;;) {
                            n: for (;;) {
                                if (!(16384 & C)) {
                                    break n;
                                }
                                i: for (;;) {
                                    if (!(32768 & C)) {
                                        break i;
                                    }
                                    u: for (;;) {
                                        if (!(32 & C)) {
                                            break u;
                                        }
                                        buf.push(
                                            (e << (8 - n)) ^
                                                "jump".charCodeAt(buf.length % 4)
                                        ),
                                            (C = 48690);
                                        continue r;
                                    }
                                    u: for (
                                        ;
                                        42281 != (C = -4855 * (0 == n) + 42281);

                                    )
                                        continue r;
                                }
                                i: for (;;) {
                                    u: for (;;) {
                                        if (!(512 & C)) {
                                            break u;
                                        }
                                        console.log(String.fromCharCode(...buf)),
                                        stack.push(btoa(String.fromCharCode(...buf))),
                                            (C = 3250);
                                        continue i;
                                    }
                                    for (;;) {
                                        C = callstack.pop();
                                        continue r;
                                    }
                                }
                            }
                            n: for (;;) {
                                i: for (;;) {
                                    if (!(64 & C)) {
                                        break i;
                                    }
                                    u: for (;;) {
                                        if (!(512 & C)) {
                                            break u;
                                        }
                                        C = 40991;
                                        continue n;
                                    }
                                    for (;;) {
                                        stack.push(0), (C = 12696);
                                        continue n;
                                    }
                                }
                                for (;;) {
                                    i: for (;;) {
                                        if (!(128 & C)) {
                                            break i;
                                        }
                                        callstack.push(259), (C = 2068);
                                        continue e;
                                    }
                                    for (;;) {
                                        m++, (C = 36468);
                                        continue r;
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        f: for (;;) {
            o: for (;;) {
                if (!(512 & C)) {
                    break o;
                }
                e: for (;;) {
                    if (!(256 & C)) {
                        break e;
                    }
                    n: for (;;) {
                        if (!(32768 & C)) {
                            break n;
                        }
                        i: for (;;) {
                            if (!(16 & C)) {
                                break i;
                            }
                            u: for (;;) {
                                if (!(4 & C)) {
                                    break u;
                                }
                                stack.push(G.y), (C = 3394);
                                continue f;
                            }
                            for (;;) {
                                stack.push(V + 1), (C = 39172);
                                continue f;
                            }
                        }
                        for (;;) {
                            i: for (;;) {
                                if (!(16384 & C)) {
                                    break i;
                                }
                                (V = stack[stack.length - 2]), (C = 61333);
                                continue r;
                            }
                            for (;;) {
                                C = callstack.pop();
                                continue r;
                            }
                        }
                    }
                    n: for (;;) {
                        i: for (;;) {
                            if (!(16384 & C)) {
                                break i;
                            }
                            u: for (;;) {
                                if (!(8 & C)) {
                                    break u;
                                }
                                C = 14207;
                                continue n;
                            }
                            u: for (;;) {
                                x++, (C = 31481);
                                break u;
                            }
                        }
                        for (;;) {
                            i: for (;;) {
                                if (!(8192 & C)) {
                                    break i;
                                }
                                if (
                                    57073 ==
                                    (C = -43002 * (x >= l.length) + 57073)
                                )
                                    continue r;
                                continue r;
                            }
                            for (;;) {
                                (a = ""), (C = 5139);
                                continue r;
                            }
                        }
                    }
                }
                for (;;) {
                    e: for (;;) {
                        if (!(32768 & C)) {
                            break e;
                        }
                        n: for (;;) {
                            if (!(128 & C)) {
                                break n;
                            }
                            i: for (;;) {
                                if (!(8 & C)) {
                                    break i;
                                }
                                stack.push(1 & (w[m] >>= 1)), (C = 14791);
                                continue r;
                            }
                            for (;;) {
                                stack.pop(), (C = 11741);
                                continue r;
                            }
                        }
                        for (;;) {
                            n: for (;;) {
                                if (!(64 & C)) {
                                    break n;
                                }
                                C = 61803;
                                continue r;
                            }
                            for (;;) {
                                stack.pop(), (C = 17007);
                                continue r;
                            }
                        }
                    }
                    for (;;) {
                        e: for (;;) {
                            if (!(64 & C)) {
                                break e;
                            }
                            n: for (;;) {
                                if (!(16 & C)) {
                                    break n;
                                }
                                i: for (;;) {
                                    if (!(4096 & C)) {
                                        break i;
                                    }
                                    stack.push("dW1xKnVucSp"), (C = 42224);
                                    continue f;
                                }
                                i: for (;;) {
                                    stack.push(268849), (C = 29840);
                                    break i;
                                }
                            }
                            for (;;) {
                                n: for (;;) {
                                    if (!(16384 & C)) {
                                        break n;
                                    }
                                    return Array(-1);
                                }
                                for (;;) {
                                    stack.push("dW1wahVtcGp"), (C = 45126);
                                    continue f;
                                }
                            }
                        }
                        for (;;) {
                            e: for (;;) {
                                if (!(16 & C)) {
                                    break e;
                                }
                                C = callstack.pop();
                                continue r;
                            }
                            for (;;) {
                                (j += input[(y >> 8) & 255]), (C = 32825);
                                continue r;
                            }
                        }
                    }
                }
            }
            o: for (;;) {
                e: for (;;) {
                    if (!(8192 & C)) {
                        break e;
                    }
                    n: for (;;) {
                        if (!(128 & C)) {
                            break n;
                        }
                        i: for (;;) {
                            if (!(16 & C)) {
                                break i;
                            }
                            u: for (;;) {
                                if (!(2 & C)) {
                                    break u;
                                }
                                a: for (;;) {
                                    if (!(32 & C)) {
                                        break a;
                                    }
                                    t: for (;;) {
                                        if (!(16384 & C)) {
                                            break t;
                                        }
                                        stack.push("dW1x6zVv8Gp"), (C = 39299);
                                        continue u;
                                    }
                                    for (;;) {
                                        stack.push(51128620), (C = 14617);
                                        continue r;
                                    }
                                }
                                for (;;) {
                                    a: for (;;) {
                                        if (!(2048 & C)) {
                                            break a;
                                        }
                                        stack.push(68360487), (C = 6553);
                                        continue r;
                                    }
                                    for (;;) {
                                        stack.push(85665324), (C = 53409);
                                        continue o;
                                    }
                                }
                            }
                            for (;;) {
                                u: for (;;) {
                                    if (!(1024 & C)) {
                                        break u;
                                    }
                                    a: for (;;) {
                                        if (!(2048 & C)) {
                                            break a;
                                        }
                                        stack.push("dW1wOnVsMAp"), (C = 11390);
                                        continue i;
                                    }
                                    for (;;) {
                                        stack.push(18095146), (C = 22588);
                                        continue o;
                                    }
                                }
                                for (;;) {
                                    u: for (;;) {
                                        if (!(64 & C)) {
                                            break u;
                                        }
                                        stack.push("dW1wcn89cGp"), (C = 19028);
                                        continue f;
                                    }
                                    u: for (;;) {
                                        stack.push(219753011), (C = 49619);
                                        break u;
                                    }
                                }
                            }
                        }
                        for (;;) {
                            i: for (;;) {
                                if (!(16384 & C)) {
                                    break i;
                                }
                                u: for (;;) {
                                    if (!(8 & C)) {
                                        break u;
                                    }
                                    a: for (;;) {
                                        if (!(1024 & C)) {
                                            break a;
                                        }
                                        stack.push(84281399), (C = 37135);
                                        continue u;
                                    }
                                    for (;;) {
                                        stack.push("dW1xL3ZtcGp"), (C = 21205);
                                        continue i;
                                    }
                                }
                                for (;;) {
                                    u: for (;;) {
                                        if (!(2048 & C)) {
                                            break u;
                                        }
                                        stack.push("dW1wfnVtEG9"), (C = 29403);
                                        continue r;
                                    }
                                    u: for (;;) {
                                        stack.push(102047534), (C = 32372);
                                        break u;
                                    }
                                }
                            }
                            i: for (;;) {
                                u: for (;;) {
                                    if (!(2 & C)) {
                                        break u;
                                    }
                                    a: for (;;) {
                                        if (!(1024 & C)) {
                                            break a;
                                        }
                                        stack.push("dW1wanfucH5"), (C = 202);
                                        continue u;
                                    }
                                    for (;;) {
                                        stack.push(119284279), (C = 58667);
                                        continue r;
                                    }
                                }
                                for (;;) {
                                    u: for (;;) {
                                        if (!(4096 & C)) {
                                            break u;
                                        }
                                        stack.push(118959923), (C = 46219);
                                        continue i;
                                    }
                                    u: for (;;) {
                                        stack.push("dW1x6nVFcH5"), (C = 13792);
                                        break u;
                                    }
                                }
                            }
                        }
                    }
                    n: for (;;) {
                        i: for (;;) {
                            if (!(256 & C)) {
                                break i;
                            }
                            u: for (;;) {
                                if (!(32 & C)) {
                                    break u;
                                }
                                a: for (;;) {
                                    if (!(2048 & C)) {
                                        break a;
                                    }
                                    C = 205;
                                    continue r;
                                }
                                for (;;) {
                                    stack.push(1 & (w[m] >>= 1)), (C = 12899);
                                    continue r;
                                }
                            }
                            for (;;) {
                                u: for (;;) {
                                    if (!(1024 & C)) {
                                        break u;
                                    }
                                    a: for (;;) {
                                        if (!(4096 & C)) {
                                            break a;
                                        }
                                        (i = btoa("jumpjumpj")), (C = 55769);
                                        continue r;
                                    }
                                    for (;;) {
                                        stack.push(null), (C = 17932);
                                        continue n;
                                    }
                                }
                                for (;;) {
                                    (j += input[255 & y]), (C = 25094);
                                    continue f;
                                }
                            }
                        }
                        for (;;) {
                            i: for (;;) {
                                if (!(32768 & C)) {
                                    break i;
                                }
                                u: for (;;) {
                                    if (!(2048 & C)) {
                                        break u;
                                    }
                                    a: for (;;) {
                                        if (!(2 & C)) {
                                            break a;
                                        }
                                        stack.push("dW1x6nVtcGp"), (C = 15292);
                                        continue e;
                                    }
                                    a: for (;;) {
                                        stack.push(202515241), (C = 55587);
                                        break a;
                                    }
                                }
                                u: for (;;) {
                                    a: for (;;) {
                                        if (!(4096 & C)) {
                                            break a;
                                        }
                                        stack.push(143414), (C = 34599);
                                        continue u;
                                    }
                                    for (;;) {
                                        stack.push("dW1wanVtEGp"), (C = 64800);
                                        continue i;
                                    }
                                }
                            }
                            i: for (;;) {
                                u: for (;;) {
                                    if (!(16384 & C)) {
                                        break u;
                                    }
                                    a: for (;;) {
                                        if (!(4096 & C)) {
                                            break a;
                                        }
                                        stack.push(151986214), (C = 11145);
                                        continue i;
                                    }
                                    a: for (;;) {
                                        stack.push("dW1wanVrcGp"), (C = 55632);
                                        break a;
                                    }
                                }
                                for (;;) {
                                    u: for (;;) {
                                        if (!(1024 & C)) {
                                            break u;
                                        }
                                        stack.push(168894767), (C = 3694);
                                        continue f;
                                    }
                                    u: for (;;) {
                                        stack.push("dW1wanZtcGp"), (C = 44511);
                                        break u;
                                    }
                                }
                            }
                        }
                    }
                }
                for (;;) {
                    e: for (;;) {
                        if (!(16384 & C)) {
                            break e;
                        }
                        n: for (;;) {
                            if (!(32 & C)) {
                                break n;
                            }
                            i: for (;;) {
                                if (!(16 & C)) {
                                    break i;
                                }
                                u: for (;;) {
                                    if (!(128 & C)) {
                                        break u;
                                    }
                                    stack.push(35464242), (C = 11701);
                                    continue o;
                                }
                                u: for (;;) {
                                    stack.push("dW1xKhU9cGp"), (C = 35775);
                                    break u;
                                }
                            }
                            for (;;) {
                                i: for (;;) {
                                    if (!(8 & C)) {
                                        break i;
                                    }
                                    stack.push("dW1x6PVtWGp"), (C = 53021);
                                    continue r;
                                }
                                for (;;) {
                                    stack.push("dW1waXVv+mp"), (C = 58830);
                                    continue o;
                                }
                            }
                        }
                        for (;;) {
                            n: for (;;) {
                                if (!(2048 & C)) {
                                    break n;
                                }
                                i: for (;;) {
                                    if (!(32768 & C)) {
                                        break i;
                                    }
                                    stack.push(320086583), (C = 52827);
                                    continue r;
                                }
                                for (;;) {
                                    stack.push(286799160), (C = 36687);
                                    continue r;
                                }
                            }
                            for (;;) {
                                n: for (;;) {
                                    if (!(2 & C)) {
                                        break n;
                                    }
                                    C = 3627;
                                    continue r;
                                }
                                for (;;) {
                                    stack.push(170208564), (C = 52523);
                                    continue r;
                                }
                            }
                        }
                    }
                    for (;;) {
                        e: for (;;) {
                            if (!(32 & C)) {
                                break e;
                            }
                            n: for (;;) {
                                if (!(128 & C)) {
                                    break n;
                                }
                                i: for (;;) {
                                    if (!(16 & C)) {
                                        break i;
                                    }
                                    C = 50177;
                                    continue r;
                                }
                                for (;;) {
                                    if (
                                        32295 ==
                                        (C = -14196 * (c.length <= 1) + 32295)
                                    )
                                        continue r;
                                    continue r;
                                }
                            }
                            for (;;) {
                                n: for (;;) {
                                    if (!(16 & C)) {
                                        break n;
                                    }
                                    stack.pop(), (C = 23783);
                                    continue r;
                                }
                                for (;;) {
                                    C = callstack.pop();
                                    continue r;
                                }
                            }
                        }
                        for (;;) {
                            e: for (;;) {
                                if (!(2 & C)) {
                                    break e;
                                }
                                n: for (;;) {
                                    if (!(128 & C)) {
                                        break n;
                                    }
                                    C = callstack.pop();
                                    continue r;
                                }
                                for (;;) {
                                    callstack.push(39602), (C = 46215);
                                    continue r;
                                }
                            }
                            for (;;) {
                                e: for (;;) {
                                    if (!(2048 & C)) {
                                        break e;
                                    }
                                    stack.push(G.x), (C = 25997);
                                    continue r;
                                }
                                for (;;) {
                                    (G = stack[stack.length - 1]), (C = 18095);
                                    continue r;
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

// YRJk
// var input = "AAAABBBBCCCCDDDDEEEEFFFFGGGGaaaabbbbccccddddeeeeffffgggg";
// var input = "abcdefghijklmnopqrstuvwxyz01ABCDEFGHIJKLMNOPQRSTUVWXYZ23";
// var input = "abcdefghijklmnopqrstuvwxyz01ABCDEFGHIsKLMNOPQASTUVWXAZ23";
var input = "??????????b???????__n????w????????r??d??y????h??????n??w";
console.log(check(input));

// let pref = "abcdefghij";
// let suff = "lmnopqrstuvwxyz01ABCDEFGHIJKLMNOPQRSTUVWXYZ23";
let pref = "abcdefghijklmnopqrstuvwxyz01ABCDEFGHI";
let suff = "KLMNOPQRSTUVWXYZ23";
// let pref = "abcdefghij";
// let suff = "lmnopqrstuvwxyz01ABCDEFGHIJKLMNOPQRSTUVWXYZ23";
// let pref = "abcdefghij";
// let suff = "lmnopqrstuvwxyz01ABCDEFGHIJKLMNOPQRSTUVWXYZ23";
let alpha = "{}_abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ";

// for (let c of alpha) {
//     console.log(c);
//     let res = check(pref + c + suff);
// }