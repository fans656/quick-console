20140821 10:47:43
实现了对 enclosing-modifier + type-in 的解析

enclosing-modifier:
    abBA -> a(b)
    a__a
     bb

type-in:
    aAbB -> ab    abAB -> ab
    aa            a_a       
      bb           b_b      

此外还有 holding-modifier 未实现解析，因为与 type-in 有冲突：
    abAB -> a~b
    a_a
     b_b
其语义为 modifiee 按下时，modifier 处于 down 状态
