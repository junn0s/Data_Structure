#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>


typedef struct ListNode {
    int item;
    struct ListNode* next;
} ListNode;
 
typedef struct LinkedListBasic {
    ListNode* head;
    ListNode* tail;
    int size;
} LinkedListBasic;

ListNode* create_node(int newItem) {
    ListNode* new_node = (ListNode*)malloc(sizeof(ListNode));
    if (new_node != NULL) {
        new_node->item = newItem;
        new_node->next = NULL;
    }
    return new_node;
}

void init_linked_list(LinkedListBasic* list) {
    list->head = NULL;
    list->tail = NULL;
    list->size = 0;
}

void append(LinkedListBasic* list, int newItem) {
    ListNode* new_node = create_node(newItem);
    if (new_node != NULL) {
        if (list->tail == NULL) {
            list->head = new_node;
            list->tail = new_node;
        } else {
            list->tail->next = new_node;
            list->tail = new_node;
        }
        list->size++;
    }
}

void remove_item(LinkedListBasic* list, int newItem) {
    ListNode* current = list->head;
    ListNode* prev = NULL;
    while (current != NULL) {
        if (current->item == newItem) {
            if (prev != NULL) {
                prev->next = current->next;
            } else {
                list->head = current->next;
            }
            if (current == list->tail) {
                list->tail = prev;
            }
            free(current);
            list->size--;
            return;
        }
        prev = current;
        current = current->next;
    }
}

bool contains(LinkedListBasic* list, int newItem) {
    ListNode* current = list->head;
    while (current != NULL) {
        if (current->item == newItem) {
            return true;
        }
        current = current->next;
    }
    return false;
}

int size(LinkedListBasic* list) {
    return list->size;
}