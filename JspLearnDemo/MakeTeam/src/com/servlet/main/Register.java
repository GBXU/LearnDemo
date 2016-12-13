package com.servlet.main;

import java.io.IOException;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.List;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;

import com.mysql.jdbc.Connection;
import com.mysql.jdbc.Statement;
import com.servlet.bean.UserBean;
import com.servlet.util.Dbutil;

/**
 * Servlet implementation class Register
 */
@WebServlet("/Register")
public class Register extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public Register() {
        super();
        // TODO Auto-generated constructor stub
    }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		// TODO Auto-generated method stub
		response.getWriter().append("Served at: ").append(request.getContextPath());
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {

        HttpSession session = request.getSession(true);
        request.setCharacterEncoding("UTF-8");
        String NA = request.getParameter("NA"); 
		String EM = request.getParameter("EM"); 
        String PW= request.getParameter("PW");
        int userid=0;
        List<String> AB = new ArrayList<String>();
        List<String> TA = new ArrayList<String>();
        if (request.getParameter("AB1")==null||request.getParameter("TA1")==null
        		||request.getParameter("AB1")==""
        		||request.getParameter("TA1")=="") {
        	getServletContext().getRequestDispatcher("/allprojects.jsp").forward(request, response);
            return;
		}
        if (request.getParameter("AB1")!="") {
            AB.add(request.getParameter("AB1"));	
		}
        if (request.getParameter("AB2")!="") {
            AB.add(request.getParameter("AB2"));	
		}
        if (request.getParameter("AB3")!="") {
            AB.add(request.getParameter("AB3"));	
		}
        
        if (request.getParameter("TA1")!="") {
            TA.add(request.getParameter("TA1"));	
		}
        if (request.getParameter("TA2")!="") {
            TA.add(request.getParameter("TA2"));	
		}
        if (request.getParameter("TA3")!="") {
            TA.add(request.getParameter("TA3"));	
		}
        response.setContentType("text/html; charset=UTF-8");  
        try {  
            Connection con=(Connection) Dbutil.getConnection();  
            String insertuser = "insert into user(name,email,password) values(?,?,?)";
            PreparedStatement userPreStmt = con.prepareStatement(insertuser);
            userPreStmt.setString(1, NA);
            userPreStmt.setString(2,EM);
            userPreStmt.setString(3,PW);
            int userRs=userPreStmt.executeUpdate(); 
	        if(userRs!=0) {  
	        	String queryuser = "select userId,name,email from user where email=?";
	            PreparedStatement queryuserPreStmt = con.prepareStatement(queryuser);
	            queryuserPreStmt.setString(1, EM);
	            ResultSet queryRs=queryuserPreStmt.executeQuery();
	            if (queryRs.next()) {
					userid = queryRs.getInt(1);
		    		UserBean user = new UserBean();
		    		user.setUserId(queryRs.getInt(1));
		    		user.setName(queryRs.getString(2));
		    		user.setEmail(queryRs.getString(3));
		    		session.setAttribute("user",user);
				}
	        }

        	String inserttab = "insert into usertab(userid,tab) values(?,?)";
            PreparedStatement inserttabPreStmt = con.prepareStatement(inserttab);
            for(String tmp:TA){
            	inserttabPreStmt.setInt(1, userid);
                inserttabPreStmt.setString(2, tmp);
                int inserttabRs=inserttabPreStmt.executeUpdate();
            }
            
        	String inserab = "insert into userability(userid,ability) values(?,?)";
            PreparedStatement inserabPreStmt = con.prepareStatement(inserab);
            for(String tmp:AB){
            	inserabPreStmt.setInt(1, userid);
                inserabPreStmt.setString(2, tmp);
                int inserabRs=inserabPreStmt.executeUpdate();
            }
        }  
        catch(Exception ex) {  
            ex.printStackTrace();  
        }  
        finally {  
        	Dbutil.Close();  
        }
        
        getServletContext().getRequestDispatcher("/allprojects.jsp").forward(request, response);
        //response.sendRedirect("allprojects.jsp");
	}

}
