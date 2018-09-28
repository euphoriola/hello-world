
#include <stdlib.h>
#include <sys/time.h>


#include <stdio.h>


int invoke_random(int min, int max, int edge)
{
    struct timeval tv;
    unsigned int range = max - min + 1;
    int random;

    if (gettimeofday(&tv, NULL) != 0) {
        printf("gettimeofday failed and may lead the random seed unchanged\n");
    }
    srand(tv.tv_usec);

    if (edge == 0) {
        random = min + (rand() % range);
    } else {
        random = rand() % (3*range) - range;
        if (random < 0) {
            random = min;
        } else if (random > (range - 1)) {
            random = max;
        } else {
            random += min;
        }
    }

    return random;
}

int man_in_bar(int r, int bar)
{
    int min;
    int max;
    switch (bar) {
        case 1:
            min = 71;
            max = 100;
        break;
        case 2:
            min = 41;
            max = 70;
        break;
        case 3:
            min = 11;
            max = 40;
        break;
        default:
            printf("wtf?!\n");
        break;
    }

    if (min <= r && r <= max) {
        return 1;
    }
    else {
        return 0;
    }
}

int main()
{
    int rlt;
    int bar;
    int bar1;
    int bar2;
    int a = 0;
    int b = 0;
    int c = 0;
    int h = 0;
    double drunk = 0;
    double home = 0;
    int i;
    for (i = 0; i < 100000; i++) {
        bar = invoke_random(1, 3, 0);
        rlt = invoke_random(1, 100, 0);
        // printf("%d\n", invoke_random(1, 100, 0));
        if (0 <= rlt && rlt <= 10) { /*the drunk man in home*/
            h++;
        }
        else if (11 <= rlt && rlt <= 40) { /*the drunk man in bar C*/
            c++;
        }
        else if (41 <= rlt && rlt <= 70) { /*the drunk man in bar B*/
            b++;
        }
        else if (71 <= rlt && rlt <= 100) { /*the drunk man in bar A*/
            a++;
        }
        else {
            /* code */
        }

        switch (bar) {
            case 1: /*police will check bar B and C*/
                bar1 = 2;
                bar2 = 3;
            break;
            case 2: /*police will check bar A and C*/
                bar1 = 1;
                bar2 = 3;
            break;
            case 3: /*police will check bar A and B*/
                bar1 = 1;
                bar2 = 2;
            break;
        }

        //start
        if ((0 == man_in_bar(rlt, bar1)) && (0 == man_in_bar(rlt, bar2))) { /*man not in bar1 or bar2*/
            if (10 < rlt) { /*the man is drunk*/
                drunk += 1.0f;
            } else {
                home += 1.0f;
            }
        }

    }
    printf("-----------------------------------------------------------\n");
    printf("a: %d\n", a);
    printf("b: %d\n", b);
    printf("c: %d\n", c);
    printf("h: %d\n", h);
    printf("%f\n", (drunk/(drunk+home)));
    // for (i = 0; i < 30000; i++) {
    //     rlt = invoke_random(3, 99, 1);
    //     if (rlt < 3) {
    //         printf("%d\n", rlt);
    //     } else if (rlt > 99) {
    //         printf("%d\n", rlt);
    //     } else {
    //         /* code */
    //     }
    // }
    printf("-----------------------------------------------------------\n");
    return 0;
}
