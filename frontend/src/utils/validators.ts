export class Validators {
    static isEmail(email: string): boolean {
        const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
        return regex.test(email)
    }

    static isPhone(phone: string): boolean {
        const regex = /^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/
        return regex.test(phone)
    }

    static minLength(value: string, length: number): boolean {
        return value.length >= length
    }

    static maxLength(value: string, length: number): boolean {
        return value.length <= length
    }

    static isRequired(value: any): boolean {
        if (typeof value === 'string') return value.trim().length > 0
        return value !== null && value !== undefined
    }

    static isPositiveNumber(value: number): boolean {
        return value > 0 && !isNaN(value)
    }

    static isBetween(value: number, min: number, max: number): boolean {
        return value >= min && value <= max
    }
}
