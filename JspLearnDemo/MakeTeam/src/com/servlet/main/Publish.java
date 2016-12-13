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
 * Servlet implementation class Publish
 */
@WebServlet("/Publish")
public class Publish extends HttpServlet {
	private static final long serialVersionUID = 1L;
       
    /**
     * @see HttpServlet#HttpServlet()
     */
    public Publish() {
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

		int projectid = 0;
		HttpSession session = request.getSession(true);
		UserBean user = (UserBean)session.getAttribute("user");
		if(user==null){
			getServletContext().getRequestDispatcher("/allprojects.jsp").forward(request, response);
		}
		
		request.setCharacterEncoding("UTF-8");
        String NA = request.getParameter("NA");
		String DE = request.getParameter("DE");
        List<String> AB = new ArrayList<String>();
        List<String> TA = new ArrayList<String>();
        if (request.getParameter("AB1")==null||request.getParameter("TA1")==null
        		||request.getParameter("AB1")==""
        		||request.getParameter("NA")==""
        		||request.getParameter("DE")=="") {
        	getServletContext().getRequestDispatcher("/profile.jsp").forward(request, response);
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

        try {
            Connection con=(Connection) Dbutil.getConnection();  
            
            String sql = "insert into project(status,leaderid,projectname,details) values(1,?,?,?)";
            PreparedStatement stmt = con.prepareStatement(sql);
            stmt.setInt(1, user.getUserId());
            stmt.setString(2,NA);
            stmt.setString(3,DE);
            int rs=stmt.executeUpdate(); 
	        if(rs==0) {
	        	getServletContext().getRequestDispatcher("/allprojects.jsp").forward(request, response);
	        }else {
	        	String sql1 = "select projectid from project where status=1 and leaderid=? and projectname=? and details=?";
	            PreparedStatement stmt1 = con.prepareStatement(sql1);
	            stmt1.setInt(1, user.getUserId());
	            stmt1.setString(2,NA);
	            stmt1.setString(3,DE);
	            ResultSet rs1=stmt1.executeQuery();
	            if (rs1.next()) {
	            	projectid = rs1.getInt(1);
				}	
			}
	        
	        
        	String sql1 = "insert into projecttab(projectid,tab) values(?,?)";
            PreparedStatement stmt1 = con.prepareStatement(sql1);
            for(String tmp:TA){
            	stmt1.setInt(1, projectid);
            	stmt1.setString(2, tmp);
                int rs1=stmt1.executeUpdate();
            }
            
        	
        	String sql2 = "insert into projectneed(projectid,ability) values(?,?)";
            PreparedStatement stmt2 = con.prepareStatement(sql2);
            for(String tmp:AB){
            	stmt2.setInt(1, projectid);
            	stmt2.setString(2, tmp);
                int rs2=stmt2.executeUpdate();
            }
            
            
            String sql3 = "insert into member(projectid,userid) values(?,?)";
            PreparedStatement stmt3 = con.prepareStatement(sql3);
            stmt3.setInt(1, projectid);
            stmt3.setInt(2, user.getUserId());
            int rs3=stmt3.executeUpdate();
 
        }  
        catch(Exception ex) {  
            ex.printStackTrace();  
        }  
        finally {  
        	Dbutil.Close();  
        }
        getServletContext().getRequestDispatcher("/profile.jsp").forward(request, response);
	}

}
