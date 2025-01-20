#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <inttypes.h>
#include <stdbool.h>
#include <unistd.h>
#include <fcntl.h>
#include <termios.h>

#include "FreeRTOS.h"
#include "task.h"
#include "timers.h"
#include "semphr.h"

/* Includes locaux. */
#include "console.h"

#define mainQUEUE_LENGTH                   (2)  // Longueur de la file
#define TASK1_PERIOD_MS                    pdMS_TO_TICKS(100)    // Période de 100 ms pour la tâche 1
#define TASK2_PERIOD_MS                    pdMS_TO_TICKS(300)    // Période de 300 ms pour la tâche 2
#define TASK3_PERIOD_MS                    pdMS_TO_TICKS(400)    // Période de 400 ms pour la tâche 3
#define TASK4_PERIOD_MS                    pdMS_TO_TICKS(500)    // Période de 500 ms pour la tâche 4
#define TASK5_PERIOD_MS                    pdMS_TO_TICKS(200)     // Période de 200 ms pour la tâche 5
#define APERIODIC_TASK_DELAY_MS            pdMS_TO_TICKS(1000)      // Période de 1000 ms pour la tâche apériodique

#define TASK1_PRIORITY                     (tskIDLE_PRIORITY + 1)   // Priorité de la tâche 1
#define TASK2_PRIORITY                     (tskIDLE_PRIORITY + 2)   // Priorité de la tâche 2
#define TASK3_PRIORITY                     (tskIDLE_PRIORITY + 3)   // Priorité de la tâche 3
#define TASK4_PRIORITY                     (tskIDLE_PRIORITY + 4)   // Priorité de la tâche 4
#define TASK5_PRIORITY                     (tskIDLE_PRIORITY + 3)   // Priorité de la tâche 5
#define APERIODIC_TASK_PRIORITY            (tskIDLE_PRIORITY + 5)   // Priorité de la tâche apériodique

/* Déclaration des tâches */
static void prvPeriodicTask1(void *pvParameters);  // Tâche qui reçoit les données de la file
static void prvPeriodicTask2(void *pvParameters);  // Tâche qui convertit les températures
static void prvPeriodicTask3(void *pvParameters);  // Tâche qui multiplie les nombres entiers
static void prvPeriodicTask4(void *pvParameters);  // Tâche qui effectue une recherche binaire
static void prvPeriodicTask5(void *pvParameters);  // Tâche périodique qui attend une réinitialisation
static void prvAperiodicTask(void *pvParameters);  // Tâche qui simule une tâche aperiodique

/* File utilisée par les deux tâches */
static QueueHandle_t xQueue = NULL;

/* Sémaphore pour la gestion de la pression d'une touche */
static SemaphoreHandle_t xButtonSemaphore = NULL;

/* Liste et élément à rechercher pour la recherche binaire */
int list[50] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20,
    21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38,
    39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50};  // Liste de 50 éléments pour la recherche binaire
int element = 25;  // Élément à rechercher dans la liste

/* Fonction principale de l'application */
void ipsa_sched(void)
{
    /* Création de la file */
    xQueue = xQueueCreate(mainQUEUE_LENGTH, sizeof(uint32_t));

    // Création du sémaphore pour la gestion de la pression de touche utilisé dans la tâche 5
    xButtonSemaphore = xSemaphoreCreateBinary();

    if (xQueue != NULL && xButtonSemaphore != NULL)
    {
        /* Création des tâches périodiques */
        xTaskCreate(prvPeriodicTask1, "PT1", configMINIMAL_STACK_SIZE, NULL, TASK1_PRIORITY, NULL);
        xTaskCreate(prvPeriodicTask2, "PT2", configMINIMAL_STACK_SIZE, NULL, TASK2_PRIORITY, NULL);
        xTaskCreate(prvPeriodicTask3, "PT3", configMINIMAL_STACK_SIZE, NULL, TASK3_PRIORITY, NULL);
        xTaskCreate(prvPeriodicTask4,"PT4", configMINIMAL_STACK_SIZE, NULL, TASK4_PRIORITY, NULL);
        xTaskCreate(prvPeriodicTask5, "PT5", configMINIMAL_STACK_SIZE, NULL, TASK5_PRIORITY, NULL);

        /* Création de la tâche apériodique */
        xTaskCreate(prvAperiodicTask, "AT", configMINIMAL_STACK_SIZE, NULL, APERIODIC_TASK_PRIORITY, NULL);

        /* Démarrage des tâches */
        vTaskStartScheduler();
    }

    /* Si tout se passe bien, le noyau planificateur est maintenant en cours d'exécution,
       et la ligne suivante ne sera jamais exécutée. Si la ligne suivante est exécutée,
       cela signifie qu'il n'y avait pas assez de mémoire heap FreeRTOS disponible pour
       créer les tâches inactives et/ou de temporisation nécessaires au fonctionnement
       du port. Consultez la section sur la gestion de la mémoire sur le site Web
       FreeRTOS pour plus de détails. */
    for (;;)
    {
    }
}

/* Tâche qui reçoit les données de la file */
static void prvPeriodicTask1(void *pvParameters)
{
    for (;;)
    {
        printf("Working\n");  // Affiche "Working" à chaque exécution de la tâche
        vTaskDelay(TASK1_PERIOD_MS);  // Attend pendant la période définie pour cette tâche 
    }
}

/* Tâche qui convertit les températures */
static void prvPeriodicTask2(void *pvParameters)
{
    for (;;)
    {
        float fahrenheit = 90.0f;
        float celsius = (fahrenheit - 32.0f) * 5.0f / 9.0f;  // Conversion de Fahrenheit à Celsius
        printf("Temperature: %f°F = %f°C\n", fahrenheit, celsius);  // Affiche la température convertie
        vTaskDelay(TASK2_PERIOD_MS);  // Attend pendant la période définie pour cette tâche 
    }
}

/* Tâche qui multiplie les nombres entiers */
static void prvPeriodicTask3(void *pvParameters)
{
    int64_t a = 1234567;
    int64_t b = 9876;
    int64_t result = a * b;  // Multiplication des deux nombres

    for (;;)
    {
        printf("Multiplication: %" PRId64 " * %" PRId64 " = %" PRId64 "\n", a, b, result);  // Affiche le résultat de la multiplication
        vTaskDelay(TASK3_PERIOD_MS);  // Attend pendant la période définie pour cette tâche 
    }
}

/* Tâche qui effectue une recherche binaire */
static void prvPeriodicTask4(void *pvParameters)
{
    int left = 0;
    int right = sizeof(list) / sizeof(list[0]);
    int mid;

    for (;;)
    {
        while (left <= right)  // Tant que l'intervalle de recherche est valide
        {
            mid = (left + right) / 2;  // Calcul de l'indice du milieu

            if (list[mid] < element)  // Si l'élément au milieu est plus petit que l'élément recherché
            {
                left = mid + 1;  // Chercher dans la moitié droite
            }
            else
            {
                right = mid - 1;  // Chercher dans la moitié gauche
            }
        }

        if (list[mid] != element)  // Si l'élément n'a pas été trouvé
        {
            printf("Element %d not found\n", element);  // Affiche que l'élément n'a pas été trouvé
        }
        else
        {
            printf("Element %d found\n", element);  // Affiche que l'élément a été trouvé
        }

        vTaskDelay(TASK4_PERIOD_MS);  // Attend pendant la période définie pour cette tâche 
    }
}

/* Fonction pour vérifier si une touche a été pressée */
int kbhit(void)
{
    struct termios oldt, newt;
    int ch;
    int oldf;

    // Sauvegarder les paramètres du terminal
    tcgetattr(STDIN_FILENO, &oldt);
    newt = oldt;
    newt.c_lflag &= ~(ICANON | ECHO);  // Désactiver le mode canonique et l'écho
    tcsetattr(STDIN_FILENO, TCSANOW, &newt);
    oldf = fcntl(STDIN_FILENO, F_GETFL, 0);
    fcntl(STDIN_FILENO, F_SETFL, oldf | O_NONBLOCK);  // Rendre stdin non bloquant

    ch = getchar();

    // Restaurer les paramètres du terminal
    tcsetattr(STDIN_FILENO, TCSANOW, &oldt);
    fcntl(STDIN_FILENO, F_SETFL, oldf);

    if (ch != EOF)
    {
        ungetc(ch, stdin);  // Remettre le caractère dans le buffer stdin
        return 1;
    }

    return 0;  // Retourne 0 si aucune touche n'a été pressée
}

void simulateButtonPress(void)
{
    // Vérifier si une touche a été pressée
    if (kbhit())
    {
        char key = getchar();  // Récupérer la touche pressée
        if (key == 'r')  // Si c'est 'r', on libère le sémaphore
        {
            printf("Key 'r' detected, giving semaphore.\n");
            xSemaphoreGive(xButtonSemaphore);  // Libérer le sémaphore
        }
    }
}

/* Tâche périodique qui attend une réinitialisation */
static void prvPeriodicTask5(void *pvParameters)
{
    int reset_flag = 0;

    for (;;)
    {
        // Vérifier si la touche 'r' a été pressée
        if (xSemaphoreTake(xButtonSemaphore, pdMS_TO_TICKS(200)) == pdTRUE)
        {
            reset_flag = 1;  // Activer le RESET
            printf("RESET activated\n");  // Afficher le message de RESET
        }

        // Si le flag RESET est activé, afficher le message et réinitialiser le flag
        if (reset_flag == 1)
        {
            printf("RESET received, resetting flag.\n");
            reset_flag = 0;  // Réinitialiser le flag
        }
        else
        {
            printf("Reset flag: %d\n", reset_flag);  // Afficher l'état du flag
        }

        // Appeler simulateButtonPress() pour détecter la pression de la touche
        simulateButtonPress();

        // Attendre 200 ms avant de ré-exécuter la tâche
        vTaskDelay(TASK5_PERIOD_MS);
    }
}

/* Tâche qui simule une tâche aperiodique */
static void prvAperiodicTask(void *pvParameters)
{
    for (;;)
    {
        printf("Bonjour je suis la tache apériodique\n");  // Affiche un message pour la tâche apériodique
        vTaskDelay(APERIODIC_TASK_DELAY_MS);  // Attend pendant la période définie pour cette tâche 
    }
}