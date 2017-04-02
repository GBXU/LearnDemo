package com.exam.main;

import java.io.*;
import java.util.*;
public class Main{
	public static void main(String[] args){
		BooleanSearch test = new BooleanSearch();
		while(true){
			test.SearchInput();
		}
	}
}

class BooleanSearch{
	private static LinkedHashMap<String, LinkedHashSet<Integer>> invertedFile;
	public BooleanSearch() {
		MyInvertedFileBuilder();
		invertedFile = ReadInvertedFile();
	}
	public void SearchInput() {
		Scanner input = new Scanner(System.in);
		String query = input.nextLine();
		Object[] root = ConstructQueryTree(query);
		System.out.println(SearchBinaryTree(root));
	}
	private Object[] ConstructQueryTree(String query) {
		//不含括号等优先级的判断
		String[] elements = query.toLowerCase().split(" ");
		ArrayList<Object[]> lastGroup = new ArrayList<>();
		for (int i = 0; i < elements.length; i++) {
			Object[] node = new Object[3];
			if (elements[i].equals("and")) {
				node[0] = "AND";
				node[1] = lastGroup.get(lastGroup.size()-1);
				lastGroup.remove(lastGroup.size()-1);
				
				Object[] rightNode = new Object[3];
				rightNode[0] = elements[i+1];
				rightNode[1] = rightNode[2] = null;
				
				node[2] = rightNode;
				i++;
			}else{
				node[0] = elements[i];
				node[1] = node[2] = null;
			}
			lastGroup.add(node);
		}
		
		Object[] lastNode = lastGroup.get(0);
		for (int i = 1; i < lastGroup.size(); i++) {
			Object[] currNode = lastGroup.get(i);
			Object[] oRNode = new Object[3];
			oRNode[0] = "OR";
			oRNode[1] = lastNode;
			oRNode[2] = currNode;
			lastNode = oRNode;
		}
		
		return lastNode;
	}
	public LinkedHashSet<Integer> SearchBinaryTree(Object[] rootNote) {
		LinkedHashSet<Integer> result = new LinkedHashSet<>();
		String keyword = rootNote[0].toString();
		if (keyword.equals("AND")) {
			LinkedHashSet<Integer> leftResult = SearchBinaryTree((Object[])rootNote[1]);
			LinkedHashSet<Integer> rightResult = SearchBinaryTree((Object[])rootNote[2]);
			for (Integer integer : leftResult) {
				if (rightResult.contains(integer)) {
					result.add(integer);
				}
			}
		}else if (keyword.equals("OR")) {
			LinkedHashSet<Integer> leftResult = SearchBinaryTree((Object[])rootNote[1]);
			LinkedHashSet<Integer> rightResult = SearchBinaryTree((Object[])rootNote[2]);
			for (Integer integer : leftResult) {
				if (!result.contains(integer)) {
					result.add(integer);
				}
			}
			for (Integer integer : rightResult) {
				if (!result.contains(integer)) {
					result.add(integer);
				}
			}
			
		}else {
			return SearchSingleKeyword(keyword);
		}
		return result;
	}
	private LinkedHashSet<Integer>  SearchSingleKeyword(String keyword) {
		if (invertedFile.containsKey(keyword)) {
			return invertedFile.get(keyword);
		}else {
			return null;
		}
	}
	private LinkedHashMap<String, LinkedHashSet<Integer>> ReadInvertedFile() {
		File file = new File("InvertedFile.txt");
		LinkedHashMap<String, LinkedHashSet<Integer>> invertedFile = new LinkedHashMap<>();
		try {
			FileInputStream stream = new FileInputStream(file);
			InputStreamReader adapter = new InputStreamReader(stream);
			BufferedReader reader = new BufferedReader(adapter);
			String line = null;
			String[] keyvalue;
			while((line = reader.readLine()) != null){
				keyvalue = line.split(":");
				if (keyvalue.length == 2) {
					String key = keyvalue[0];
					String value = keyvalue[1];
					LinkedHashSet<Integer> values = new LinkedHashSet<>();
					String[] valuestr = value.split("[^0-9]");
					for (int i = 0; i < valuestr.length; i++) {
						if (!valuestr[i].equals("")) {
							values.add(new Integer(valuestr[i]));
						}
					}
					invertedFile.put(key, values);
				}
			}
			reader.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
		return invertedFile;
	}
	private static void MyInvertedFileBuilder(){
		File dir = new File("documents");
		File[] files = dir.listFiles();
		LinkedHashMap<Integer, String> src = new LinkedHashMap<>();
		LinkedHashMap<String, LinkedHashSet<Integer>> invertedFile = new LinkedHashMap<>();
		for (int id = 0; id < files.length; id++) {
			File in = files[id];
			if(in.isFile()){
				try {
					FileInputStream fileInputStream = new FileInputStream(in);//InputStream
					InputStreamReader read = new InputStreamReader(fileInputStream,"GBK");//Adapter:GBK decode
					BufferedReader bufferedReader = new BufferedReader(read);//Reader:use the buffer
					String lineTxt = new String();
					String tmp = null;
					while((tmp = bufferedReader.readLine()) != null){
						lineTxt = lineTxt + tmp;
					}
					bufferedReader.close();//close the BufferedReader and the InputStream, InputStreamReader would be closed, too.
		            
					src.put(id, lineTxt);//files ID map
					//String[] words = lineTxt.split("^[A-Za-z]");
					String[] words = lineTxt.replace(".", "").split(" |,|:|\"");
					for (String word : words) {
						if(!invertedFile.containsKey(word)){
							invertedFile.put(word,new LinkedHashSet<Integer>());
							invertedFile.get(word).add(id);
						}else {
							invertedFile.get(word).add(id);	// words inveredFile
						}
						
					}
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		}
		File out = new File("InvertedFile.txt");
		if (!out.exists()) {
			try {
				out.createNewFile();
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
		try {
			BufferedWriter output = new BufferedWriter(new FileWriter(out));
			for (String word : invertedFile.keySet()) {
				output.write(word+":"+invertedFile.get(word)+'\r'+'\n');
			}	
			output.close();
		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}