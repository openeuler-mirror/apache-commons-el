%global base_name       el
%global short_name      commons-%{base_name}
Name:                apache-%{short_name}
Version:             1.0
Release:             1
Summary:             The Apache Commons Extension Language
License:             ASL 1.1
URL:                 http://commons.apache.org/el
BuildArch:           noarch
Source0:             http://archive.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Source1:             https://repo1.maven.org/maven2/%{short_name}/%{short_name}/%{version}/%{short_name}-%{version}.pom
Patch0:              %{short_name}-%{version}-license.patch
Patch1:              %{short_name}-eclipse-manifest.patch
Patch2:              %{short_name}-enum.patch
BuildRequires:       ant junit javapackages-local apache-commons-logging glassfish-jsp-api
BuildRequires:       glassfish-servlet-api

%description
An implementation of standard interfaces and abstract classes for
javax.servlet.jsp.el which is part of the JSP 2.0 specification.

%package        javadoc
Summary:             API documentation for %{name}
%description    javadoc
%{summary}.

%prep
%setup -q -n %{short_name}-%{version}-src
%patch0 -p1 -b .license
%patch1 -p1
%patch2 -p1
find . -type f -name "*.jar" -exec rm -f {} \;
cat > build.properties <<EOBP
build.compiler=modern
junit.jar=$(build-classpath junit)
servlet-api.jar=$(build-classpath glassfish-servlet-api)
jsp-api.jar=$(build-classpath glassfish-jsp-api)
servletapi.build.notrequired=true
jspapi.build.notrequired=true
EOBP
find . -iname 'ELParser.java' -exec sed -i 's:enum:enum1:g' \{\} \;

%build
export CLASSPATH=
export OPT_JAR_LIST=:
%{ant} \
  -Dfinal.name=%{short_name} \
  -Dj2se.javadoc=%{_javadocdir}/java \
  jar javadoc

%install
%mvn_artifact %{SOURCE1} dist/%{short_name}.jar
%mvn_alias "commons-el:commons-el" "org.apache.commons:commons-el"
%mvn_file : %{name} %{short_name}
%mvn_install -J dist/docs/api

%files -f .mfiles
%license LICENSE.txt
%doc STATUS.html

%files javadoc -f .mfiles-javadoc
%license LICENSE.txt

%changelog
* Sat Jul 25 2020 chengzihan <chengzihan2@huawei.com> - 1.0-1
- Package init
