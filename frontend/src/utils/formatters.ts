export class Formatters {
    static price(value: number): string {
        return `${value.toLocaleString('ru-RU')}₽`
    }

    static rating(value: number): string {
        return `⭐ ${value.toFixed(1)}`
    }

    static reviewCount(count: number): string {
        return `(${count} ${this.pluralize(count, 'отзыв', 'отзыва', 'отзывов')})`
    }

    static date(date: Date | string): string {
        const d = typeof date === 'string' ? new Date(date) : date
        return d.toLocaleDateString('ru-RU', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        })
    }

    static time(date: Date | string): string {
        const d = typeof date === 'string' ? new Date(date) : date
        return d.toLocaleTimeString('ru-RU', {
            hour: '2-digit',
            minute: '2-digit'
        })
    }

    static truncate(text: string, length: number = 100): string {
        return text.length > length ? text.substring(0, length) + '...' : text
    }

    private static pluralize(num: number, one: string, two: string, five: string): string {
        const n = num % 100
        if (n >= 11 && n <= 19) return five
        const r = num % 10
        if (r === 1) return one
        if (r >= 2 && r <= 4) return two
        return five
    }
}
