function setup() {
    {
        let e = [];
        (___ = e.shift.bind(e)),
            Object.defineProperty(___, "_", { value: Number }),
            Object.defineProperty(___, "__", { get: () => e });
    }
    {
        let a = (b) =>
                eval(
                    [...b]
                        .map((e) => String.fromCharCode(13 ^ e.charCodeAt()))
                        .join("")
                ),
            // d = [
            //     "%$03R0R&R",
            //     "%$03R0 R&R",
            //     "%$03R0R'R",
            //     "%$03vRR0R6R0R(RRp",
            //     "%$03R0RSR",
            //     "%$03R",
            //     "%$03R0-RRR#RRVRP",
            //     "%$03R0RRR#R%R00R$",
            //     "%$03vRR0R6R0RRR#R%R++RR$p",
                // "%$03RRR%$",
                // ()=>_=_+_
                // ()=>_=-_+_
                // ()=>_=_*_
                // ()=>{__=_;_=_%__}
                // ()=>_=_^_
                // ()=>_
                // ()=>_= ___.__[_]
                // ()=>_=___._(_==_)
                // ()=>{__=_;_=___._(_&&__)}
                // ()=>___()
            // ].map(a),
            e = Object.getOwnPropertyDescriptors;
        let Log = console.log;
        let Counter = 0;

        // d = [
        //     () => (_ = _ + _),
        //     () => (_ = -_ + _),
        //     () => (_ = _ * _),
        //     () => {
        //         __ = _;
        //         _ = _ % __;
        //     },
        //     () => (_ = _ ^ _),
        //     () => _,
        //     () => (_ = ___.__[_]),
        //     () => (_ = ___._(_ == _)),
        //     () => {
        //         __ = _;
        //         _ = ___._(_ && __);
        //     },
        //     () => ___(),
        // ];

        // let vmadd = () => {
        //     let tos1 = ___._(_),
        //         tos2 = ___._(_)
        //     console.log("add", tos1, tos2);
        //     _ = tos1 + tos2;
        // };

        // let vmsub = () => {
        //     let tos1 = ___._(_),
        //         tos2 = ___._(_);
        //     console.log("sub", tos1, tos2);
        //     _ = tos2 - tos1;
        // };

        // let vmmul = () => {
        //     let tos1 = ___._(_),
        //         tos2 = ___._(_);
        //     console.log("mul", tos1, tos2);
        //     _ = tos1 * tos2;
        // };

        // let vmmod = () => {
        //     let tos1 = ___._(_),
        //         tos2 = ___._(_);
        //     console.log("mod", tos1, tos2);
        //     _ = tos2 % tos1;
        // }

        // let vmxor = () => {
        //     let tos1 = ___._(_),
        //         tos2 = ___._(_);
        //     console.log("xor", tos1, tos2);
        //     _ = tos1 ^ tos2;
        // }

        // let vmpop = () => {
        //     let tos = ___._(_);
        //     console.log("pop", tos);
        //     return tos;
        // }

        // let vmload = () => {
        //     let tos = ___._(_);
        //     console.log("load", tos);
        //     _ = ___.__[tos];
        // }

        // let vmcmp = () => {
        //     let tos1 = ___._(_),
        //         tos2 = ___._(_);
        //     console.log("cmp", tos1, tos2);
        //     _ = ___._(tos1 == tos2);
        // }

        // let vmand = () => {
        //     let tos1 = ___._(_),
        //         tos2 = ___._(_);
        //     console.log("and", tos1, tos2);
        //     _ = ___._(tos1 && tos2);
        // }

        // let vmshift = () => {
        //     console.log("shift", ___());
        // }

        d = [
            // vmadd
            () => {
                let tos1 = ___._(_),
                    tos2 = ___._(_);
                // Log("add", tos1, tos2);
                _ = tos1 + tos2;
            },
            // vmsub,
            () => {
                let tos1 = ___._(_),
                    tos2 = ___._(_);
                // Log("sub", tos1, tos2);
                _ = tos2 - tos1;
            },
            // ()=>_=-_+_,
            // vmmul,
            () => {
                let tos1 = ___._(_),
                    tos2 = ___._(_);
                // Log("mul", tos1, tos2);
                _ = tos1 * tos2;
            },
            // vmmod,
            () => {
                let tos1 = ___._(_),
                    tos2 = ___._(_);
                // Log("mod", tos1, tos2);
                _ = tos2 % tos1;
            },
            // vmxor,
            () => {
                let tos1 = ___._(_),
                    tos2 = ___._(_);
                // Log("xor", tos1, tos2);
                _ = tos1 ^ tos2;
            },
            // vmpop,
            () => {
                let tos = ___._(_);
                // Log("pop", tos);
                return tos;
            },
            // vmload,
            () => {
                let tos = ___._(_);
                // Log("load", tos, ___.__[tos]);
                _ = ___.__[tos];
            },
            // vmcmp,
            () => {
                let tos1 = ___._(_),
                    tos2 = ___._(_);
                Log("cmp", tos1, tos2);
                _ = ___._(tos1 == tos2);
            },
            // vmand,
            () => {
                let tos1 = ___._(_),
                    tos2 = ___._(_);
                // Log("and", tos1, tos2);
                _ = ___._(tos1 && tos2);
            },
            // vmshift,
            () => {
                Log("shift", ___());
            },
        ];

        Object.defineProperty(window, "_", {
            // get: () => ___.__.pop(),
            // set: (e) => ___.__.push(e),
            get: () => {
                // Counter++;
                // Log("access window", _);
                Log("counter", Counter);
                return ___.__.pop();
            },
            set: (e) => {
                ___.__.push(e);
                // Log("pushed", ___.__[___.__.length - 1]);
            },
        });
        // String, Promise, console, Math
        for (const t of ["^y\x7Fdcj", "]\x7Fb`d~h", "nbc~bah", "@lye"]) {
            let R = a(t);
            const o = e("^" == t[0] ? R.prototype : R); // String.prototype only
            for (const e in o) {
                const n = o[e].value;
                if (null != n)
                    try {
                        console.log(R, e, n);
                        const o = (5 * t.length + e.length + 7) % 11;
                        Object.defineProperty(Object.prototype, e, {
                            // get: () => (d[o]?.(), n),
                            get: () => {
                                Counter++;
                                Log("access object", e, o);
                                return d[o]?.(), n;
                            },
                        }),
                            Object.defineProperty(R, e, {
                                // get: () => (d[o]?.(), n),
                                get: () => {
                                    Counter++;
                                    Log("access", R, e, o);
                                    return d[o]?.(), n;
                                },
                            });
                    } catch {}
            }
        }
        const l = a("zdcibz");
        console.log(l);
        for (const t in e(l)) {
            if (null === l[t] || void 0 === l[t]) continue;
            const e = l[t];
            try {
                const R = t.length % 16;
                // console.log(t, e, R);
                Object.defineProperty(Object.prototype, t, {
                    // get: () => ((_ = R), e),
                    get: () => {
                        Counter++;
                        Log("access object 2", t, R);
                        return (_ = R), e;
                    },
                });
                console.log(t, e, R);
            } catch {}
        }
    }
}

setup();

function dump() {
    // String, Promise, console, Math
    let attrs = {}
    for (const t of ["String", "Promise", "console", "Math"]) {
        let R = eval(t);
        const o = Object.getOwnPropertyDescriptors("S" == t[0] ? R.prototype : R); // String.prototype only
        for (const e in o) {
            const n = o[e].value;
            if (null != n) {
                const o = (5 * t.length + e.length + 7) % 11;
                // console.log(o, e);
                attrs[e] = o;
            }
        }
    }
    console.log(attrs);
}

dump();
