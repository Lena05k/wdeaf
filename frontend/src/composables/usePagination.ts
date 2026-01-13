import { ref, computed } from 'vue'

interface PaginationOptions {
    pageSize?: number
    preloadPages?: number
}

export function usePagination(options: PaginationOptions = {}) {
    const pageSize = options.pageSize || 20
    const preloadPages = options.preloadPages || 2

    const currentPage = ref<number>(1)
    const totalItems = ref<number>(0)
    const isLoading = ref<boolean>(false)

    const totalPages = computed((): number => {
        return Math.ceil(totalItems.value / pageSize)
    })

    const hasNextPage = computed((): boolean => {
        return currentPage.value < totalPages.value
    })

    const hasPrevPage = computed((): boolean => {
        return currentPage.value > 1
    })

    const startIndex = computed((): number => {
        return (currentPage.value - 1) * pageSize
    })

    const endIndex = computed((): number => {
        return Math.min(startIndex.value + pageSize, totalItems.value)
    })

    const nextPage = (): void => {
        if (hasNextPage.value) {
            currentPage.value++
        }
    }

    const prevPage = (): void => {
        if (hasPrevPage.value) {
            currentPage.value--
        }
    }

    const goToPage = (page: number): void => {
        if (page >= 1 && page <= totalPages.value) {
            currentPage.value = page
        }
    }

    const reset = (): void => {
        currentPage.value = 1
        totalItems.value = 0
    }

    return {
        currentPage,
        totalItems,
        isLoading,
        totalPages,
        hasNextPage,
        hasPrevPage,
        startIndex,
        endIndex,
        pageSize,
        preloadPages,
        nextPage,
        prevPage,
        goToPage,
        reset
    }
}
