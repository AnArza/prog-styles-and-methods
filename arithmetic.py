import struct

BIAS = 127
MASK64 = (1 << 64) - 1


class ArithmeticModule:

    @staticmethod
    def add_bits(a, b):
        a &= MASK64
        b &= MASK64

        while b != 0:
            carry = ((a & b) << 1) & MASK64
            a = (a ^ b) & MASK64
            b = carry

        return a

    @staticmethod
    def sub_bits(a, b):
        return ArithmeticModule.add_bits(
            a,
            ArithmeticModule.add_bits((~b) & MASK64, 1)
        )

    @staticmethod
    def mul_bits(a, b):
        result = 0

        while b != 0:
            if b & 1:
                result = ArithmeticModule.add_bits(result, a)

            a = (a << 1) & MASK64
            b >>= 1

        return result

    @staticmethod
    def div_bits(a, b):
        result = 0
        remainder = 0

        for i in range(63, -1, -1):
            remainder <<= 1
            remainder |= (a >> i) & 1

            if remainder >= b:
                remainder = ArithmeticModule.sub_bits(remainder, b)
                result |= 1 << i

        return result

    @staticmethod
    def float_to_bits(value):
        return struct.unpack(">I", struct.pack(">f", value))[0]

    @staticmethod
    def bits_to_float(bits):
        return struct.unpack(
            ">f",
            struct.pack(">I", bits & 0xFFFFFFFF)
        )[0]

    @staticmethod
    def exponent(bits):
        return (bits >> 23) & 0xFF

    @staticmethod
    def mantissa(bits):
        return (bits & 0x7FFFFF) | (1 << 23)

    @staticmethod
    def make_float(exponent, mantissa, negative=False):
        bits = (exponent << 23) | (mantissa & 0x7FFFFF)

        if negative:
            bits |= 0x80000000

        return ArithmeticModule.bits_to_float(bits)

    @staticmethod
    def add(a, b):
        bits_a = ArithmeticModule.float_to_bits(a)
        bits_b = ArithmeticModule.float_to_bits(b)

        exp_a = ArithmeticModule.exponent(bits_a)
        exp_b = ArithmeticModule.exponent(bits_b)

        man_a = ArithmeticModule.mantissa(bits_a)
        man_b = ArithmeticModule.mantissa(bits_b)

        # Equalize exponents
        if exp_a > exp_b:
            man_b >>= exp_a - exp_b
            exp_b = exp_a

        elif exp_b > exp_a:
            man_a >>= exp_b - exp_a
            exp_a = exp_b

        result = ArithmeticModule.add_bits(man_a, man_b)

        # Normalize mantissa
        if result & (1 << 24):
            result >>= 1
            exp_a += 1

        return ArithmeticModule.make_float(exp_a, result)

    @staticmethod
    def subtract(a, b):
        bits_a = ArithmeticModule.float_to_bits(a)
        bits_b = ArithmeticModule.float_to_bits(b)

        negative = False

        if bits_b > bits_a:
            bits_a, bits_b = bits_b, bits_a
            negative = True

        exp_a = ArithmeticModule.exponent(bits_a)
        exp_b = ArithmeticModule.exponent(bits_b)

        man_a = ArithmeticModule.mantissa(bits_a)
        man_b = ArithmeticModule.mantissa(bits_b)

        man_b >>= exp_a - exp_b

        result = ArithmeticModule.sub_bits(man_a, man_b)

        if result == 0:
            return 0.0

        # Normalize
        while (result & (1 << 23)) == 0:
            result <<= 1
            exp_a -= 1

        return ArithmeticModule.make_float(
            exp_a,
            result,
            negative
        )

    @staticmethod
    def multiply(a, b):
        bits_a = ArithmeticModule.float_to_bits(a)
        bits_b = ArithmeticModule.float_to_bits(b)

        exp_a = ArithmeticModule.exponent(bits_a)
        exp_b = ArithmeticModule.exponent(bits_b)

        man_a = ArithmeticModule.mantissa(bits_a)
        man_b = ArithmeticModule.mantissa(bits_b)

        result = ArithmeticModule.mul_bits(man_a, man_b)

        exponent = exp_a + exp_b - BIAS

        # Normalize mantissa
        if result & (1 << 47):
            result >>= 24
            exponent += 1
        else:
            result >>= 23

        return ArithmeticModule.make_float(exponent, result)

    @staticmethod
    def divide(a, b):
        bits_a = ArithmeticModule.float_to_bits(a)
        bits_b = ArithmeticModule.float_to_bits(b)

        exp_a = ArithmeticModule.exponent(bits_a)
        exp_b = ArithmeticModule.exponent(bits_b)

        man_a = ArithmeticModule.mantissa(bits_a)
        man_b = ArithmeticModule.mantissa(bits_b)

        # Extra 23 bits for division precision
        man_a <<= 23

        result = ArithmeticModule.div_bits(man_a, man_b)

        exponent = exp_a - exp_b + BIAS

        # Normalize
        if result < (1 << 23):
            result <<= 1
            exponent -= 1

        return ArithmeticModule.make_float(exponent, result)


# Example
if __name__ == "__main__":
    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))

    print("Addition:", ArithmeticModule.add(a, b))
    print("Subtraction:", ArithmeticModule.subtract(a, b))
    print("Multiplication:", ArithmeticModule.multiply(a, b))
    print("Division:", ArithmeticModule.divide(a, b))
