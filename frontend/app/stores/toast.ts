import { defineStore } from 'pinia'

export type ToastKind = 'error' | 'success' | 'info'

export interface ToastMessage {
  id: number
  kind: ToastKind
  message: string
}

interface ToastState {
  items: ToastMessage[]
  nextId: number
}

const MAX_VISIBLE_TOASTS = 4

export const useToastStore = defineStore('toast', {
  state: (): ToastState => ({ items: [], nextId: 1 }),
  actions: {
    push(message: string, kind: ToastKind = 'info'): void {
      const item = { id: this.nextId, kind, message }
      this.nextId += 1
      this.items = [...this.items, item].slice(-MAX_VISIBLE_TOASTS)
    },
    dismiss(id: number): void {
      this.items = this.items.filter(item => item.id !== id)
    },
    clear(): void {
      this.items = []
    },
  },
})
