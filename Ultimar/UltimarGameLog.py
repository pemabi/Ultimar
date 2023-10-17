class gameLog():
    def __init__(self) -> None:
            
        log = []

        def navigateLog(self, currentIndex):
                return log[currentIndex]
            
        def moveForwards(self, log, currentIndex):
            if currentIndex < (len(log) - 1):
                return log[currentIndex + 1]
            
        def logCutoff(self, log, desiredIndex):
            log = log[0:desiredIndex]

            """
            
                        [["b", "O", False, False, []], ["b", "L", False, False, []], ["b", "C", False, [], []], ["b", "W", False, False, []], 
             ["b", "K", False, False, []], ["b", "H", False, [], []], ["b", "L", False, False, []], ["b", "I", False, [('I')], []]],
            [["b", "P", False, False, []], ["b", "P", False, False, []], ["b", "P", False, False, []], ["b", "P", False, False, []], 
             ["b", "P", False, False, []], ["b", "P", False, False, []], ["b", "P", False, False, []], ["b", "P", False, False, []]],
            [[], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], []],
            [["w", "P", False, False, []], ["w", "P", False, False, []], ["w", "P", False, False, []], ["w", "P", False, False, []], 
             ["w", "P", False, False, []], ["w", "P", False, False, []], ["w", "P", False, False, []], ["w", "P", False, False, []]],
            [["w", "I", False, [('i')], []], ["w", "L", False, False, []], ["w", "C", False, [], []], ["w", "W", False, False, []], 
             ["w", "K", False, False, []], ["w", "H", False, [], []], ["w", "L", False, False, []], ["w", "O", False, False, []]]]
            
            """
