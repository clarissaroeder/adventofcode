        # Start at the root of the trie for each call
            # Iterate through all possible towel starting colours
            # for head in self.towels.root.children:
            #     print("Design:", design)
            #     print("Index:", index)
            #     print("Head:", head)
            #     input()

                # # If the current head doesnt match the current index, none of the towels beginning with that color will
                # if head != design[index]: continue

                # # For all towels beginning with this current head, find complete towels:
                # towel_colors = [head]
                # current = self.towels.root.children[head]
                # while current:
                #     print("Current:", current)
                #     print("Current children:", current.children)
                #     input()
                #     if current.end_of_towel:
                #         towel = "".join(towel_colors)
          
                #         # If complete towel, check if it fits the design at the current index
                #         if design.startswith(towel, index):
                #             candidate.append(head)  # take
                #             backtrack(design, index + len(towel), candidate, result) # explore
                #             candidate.pop() # clean up

                #     for child in current.children:
                #         print("Next color in towel:", child)
                #         input()