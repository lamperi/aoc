package elves;

import java.util.ArrayList;
import java.util.List;

/**
 * Brute force for AdventOfCode.com 2016 Day 19
 * 
 */
public class CollectionElves {

   final int n;
   
   public CollectionElves(int n) {
      this.n = n;
   }
   
   
   public void solve() {
      List<Integer> elves = new ArrayList<>();
      for (int i = 0; i < n; ++i) { elves.add(i+1); }
      int i = 0;
      while(true) {
         int j = (i+elves.size()/2) % elves.size();
         elves.remove(j);

         if (j > i) {
            i += 1;
         }
         if (i == elves.size()) {
            i = 0;
         }
         
         if (elves.size() % 1000 == 0) {
            System.out.println("Part 2: Still left : " + (elves.size()));
         }

         if (elves.size() == 1) {
            System.out.println("Part 2: Solution : " + elves);
            return;
         }
      }
   }
   
   public static void main(String[] args) {
      new CollectionElves(5).solve();
      new CollectionElves(3001330).solve();
   }
}
