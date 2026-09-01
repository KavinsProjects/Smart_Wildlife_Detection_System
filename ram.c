#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    // Calculate 4GB in bytes. 
    // Using ULL (unsigned long long) prevents integer overflow on 32-bit systems.
    size_t four_gb = 4ULL * 1024 * 1024 * 1024;

    printf("Attempting to allocate 4GB of RAM...\n");

    // Allocate the memory using malloc
    char *memory = (char *)malloc(four_gb);

    if (memory == NULL) {
        fprintf(stderr, "Memory allocation failed. Not enough contiguous memory available.\n");
        return 1;
    }

    printf("Virtual memory allocated. Writing to memory to claim physical RAM...\n");

    // Modern operating systems use "lazy allocation", meaning they only reserve virtual 
    // memory until you actually write to it. memset forces the OS to map real physical RAM.
    memset(memory, 0, four_gb);

    printf("Successfully locked 4GB of physical RAM.\n");
    printf("Press Enter to free the memory and exit...\n");

    // Keep the program running so you can verify the RAM usage in Task Manager / System Monitor
    getchar();

    // Clean up
    free(memory);
    printf("Memory freed. Exiting.\n");

    return 0;
}